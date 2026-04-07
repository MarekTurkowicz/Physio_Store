"""Order service — order management business logic."""

from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    BadRequestException,
    ForbiddenException,
    InsufficientStockException,
    NotFoundException,
)
from app.models.user import User
from app.repositories.order_repo import OrderRepository
from app.repositories.product_repo import ProductRepository
from app.schemas.order import (
    OrderCreate,
    OrderListResponse,
    OrderResponse,
    OrderStatusUpdate,
)


# Valid status transitions to enforce workflow
VALID_TRANSITIONS = {
    "pending": ["confirmed", "cancelled"],
    "confirmed": ["shipped", "cancelled"],
    "shipped": ["delivered"],
    "delivered": [],
    "cancelled": [],
}


class OrderService:
    def __init__(self, session: AsyncSession):
        self.order_repo = OrderRepository(session)
        self.product_repo = ProductRepository(session)
        self.session = session

    async def create_order(self, data: OrderCreate, user: User) -> OrderResponse:
        """
        Place a new order.
        Validates stock, calculates totals, decrements inventory.
        """
        items_data = []
        total_amount = Decimal("0.00")

        for item in data.items:
            product = await self.product_repo.get_by_id(item.product_id)
            if not product:
                raise NotFoundException(
                    message=f"Produkt nie znaleziony (ID: {item.product_id})"
                )
            if not product.is_active:
                raise BadRequestException(
                    message=f"Produkt '{product.name}' jest niedostępny"
                )
            if product.stock_quantity < item.quantity:
                raise InsufficientStockException(
                    product_name=product.name,
                    available=product.stock_quantity,
                    requested=item.quantity,
                )

            line_total = product.price * item.quantity
            total_amount += line_total

            items_data.append({
                "product_id": product.id,
                "quantity": item.quantity,
                "unit_price": product.price,
            })

            # Decrement stock
            await self.product_repo.update(
                product, stock_quantity=product.stock_quantity - item.quantity
            )

        order = await self.order_repo.create_with_items(
            user_id=user.id,
            shipping_address=data.shipping_address,
            total_amount=total_amount,
            items_data=items_data,
        )
        return OrderResponse.model_validate(order)

    async def get_order(self, order_id: int, user: User) -> OrderResponse:
        """Get order details. Users can only see their own orders."""
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise NotFoundException(message="Zamówienie nie znalezione")
        if user.role != "admin" and order.user_id != user.id:
            raise ForbiddenException(message="Brak dostępu do tego zamówienia")
        return OrderResponse.model_validate(order)

    async def list_orders(
        self, user: User, skip: int = 0, limit: int = 20
    ) -> OrderListResponse:
        """List orders — admin/manager sees all, customers see only their own."""
        if user.role in ["admin", "manager"]:
            orders, total = await self.order_repo.get_all_orders(skip=skip, limit=limit)
        else:
            orders, total = await self.order_repo.get_by_user(
                user.id, skip=skip, limit=limit
            )

        return OrderListResponse(
            items=[OrderResponse.model_validate(o) for o in orders],
            total=total,
            skip=skip,
            limit=limit,
        )

    async def update_status(
        self, order_id: int, data: OrderStatusUpdate
    ) -> OrderResponse:
        """
        Update order status (admin only).
        Enforces valid status transitions.
        If cancelled, restores stock.
        """
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise NotFoundException(message="Zamówienie nie znalezione")

        allowed = VALID_TRANSITIONS.get(order.status, [])
        if data.status not in allowed:
            raise BadRequestException(
                message=f"Nie można zmienić statusu z '{order.status}' na '{data.status}'",
                detail=f"Dozwolone przejścia: {', '.join(allowed) if allowed else 'brak'}",
            )

        # Restore stock on cancellation
        if data.status == "cancelled":
            for item in order.items:
                product = await self.product_repo.get_by_id(item.product_id)
                if product:
                    await self.product_repo.update(
                        product,
                        stock_quantity=product.stock_quantity + item.quantity,
                    )

        order = await self.order_repo.update(order, status=data.status)
        return OrderResponse.model_validate(order)

    async def cancel_order(self, order_id: int, user: User) -> OrderResponse:
        """Cancel own order (customer) — only if still pending."""
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise NotFoundException(message="Zamówienie nie znalezione")
        if user.role != "admin" and order.user_id != user.id:
            raise ForbiddenException(message="Brak dostępu do tego zamówienia")
        if order.status != "pending":
            raise BadRequestException(
                message="Można anulować tylko zamówienia ze statusem 'pending'"
            )

        return await self.update_status(
            order_id, OrderStatusUpdate(status="cancelled")
        )
