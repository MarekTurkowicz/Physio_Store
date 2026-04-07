"""
Custom exception classes for business logic errors.
These are raised by services and mapped to HTTP responses by exception_handlers.
"""


class AppException(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str, detail: str | None = None):
        self.message = message
        self.detail = detail
        super().__init__(message)


class NotFoundException(AppException):
    """Resource not found (maps to 404)."""
    pass


class AlreadyExistsException(AppException):
    """Resource already exists / duplicate (maps to 409)."""
    pass


class UnauthorizedException(AppException):
    """Authentication required or failed (maps to 401)."""
    pass


class ForbiddenException(AppException):
    """Insufficient permissions (maps to 403)."""
    pass


class BadRequestException(AppException):
    """Invalid input or business rule violation (maps to 400)."""
    pass


class InsufficientStockException(BadRequestException):
    """Not enough stock to fulfill an order."""

    def __init__(self, product_name: str, available: int, requested: int):
        super().__init__(
            message=f"Niewystarczający stan magazynowy: {product_name}",
            detail=f"Dostępne: {available}, zamówione: {requested}",
        )
