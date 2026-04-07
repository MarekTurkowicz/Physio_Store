"""
Global exception handlers — maps custom exceptions to HTTP responses.
Registered in main.py on the FastAPI app.
"""

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AlreadyExistsException,
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
)


async def not_found_handler(request: Request, exc: NotFoundException) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": exc.message, "detail": exc.detail})


async def already_exists_handler(request: Request, exc: AlreadyExistsException) -> JSONResponse:
    return JSONResponse(status_code=409, content={"message": exc.message, "detail": exc.detail})


async def unauthorized_handler(request: Request, exc: UnauthorizedException) -> JSONResponse:
    return JSONResponse(status_code=401, content={"message": exc.message, "detail": exc.detail})


async def forbidden_handler(request: Request, exc: ForbiddenException) -> JSONResponse:
    return JSONResponse(status_code=403, content={"message": exc.message, "detail": exc.detail})


async def bad_request_handler(request: Request, exc: BadRequestException) -> JSONResponse:
    return JSONResponse(status_code=400, content={"message": exc.message, "detail": exc.detail})


def register_exception_handlers(app) -> None:
    """Register all custom exception handlers on the FastAPI app."""
    app.add_exception_handler(NotFoundException, not_found_handler)
    app.add_exception_handler(AlreadyExistsException, already_exists_handler)
    app.add_exception_handler(UnauthorizedException, unauthorized_handler)
    app.add_exception_handler(ForbiddenException, forbidden_handler)
    app.add_exception_handler(BadRequestException, bad_request_handler)
