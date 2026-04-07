"""Order repository — data access for Order and OrderItem models."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order, OrderItem
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self, session: AsyncSession):
        super().__init__(Order, session)

    async def get_by_user(
        self, user_id: int, skip: int = 0, limit: int = 20
    ) -> tuple[list[Order], int]:
        """Get orders for a specific user with pagination."""
        filters = [Order.user_id == user_id]
        orders = await self.get_all(skip=skip, limit=limit, filters=filters)
        total = await self.count(filters=filters)
        return list(orders), total

    async def get_all_orders(
        self, skip: int = 0, limit: int = 20
    ) -> tuple[list[Order], int]:
        """Get all orders with pagination (admin view)."""
        orders = await self.get_all(skip=skip, limit=limit)
        total = await self.count()
        return list(orders), total

    async def create_with_items(
        self,
        user_id: int,
        shipping_address: str,
        total_amount: float,
        items_data: list[dict],
    ) -> Order:
        """Create order with its items in one operation."""
        order = Order(
            user_id=user_id,
            shipping_address=shipping_address,
            total_amount=total_amount,
            status="pending",
        )
        self.session.add(order)
        await self.session.flush()

        for item_data in items_data:
            item = OrderItem(
                order_id=order.id,
                product_id=item_data["product_id"],
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
            )
            self.session.add(item)

        await self.session.flush()
        await self.session.refresh(order)
        return order
