"""CORS configuration — explicit allowlist with dev-friendly defaults."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import Settings

_DEV_ORIGINS: tuple[str, ...] = (
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
)

_ALLOWED_METHODS: tuple[str, ...] = ("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS")

_ALLOWED_HEADERS: tuple[str, ...] = (
    "Authorization",
    "Content-Type",
    "Accept",
    "Accept-Language",
    "X-Requested-With",
)

_PREFLIGHT_MAX_AGE_SECONDS = 600


class CORSConfigurationError(RuntimeError):
    """Raised when CORS cannot be configured safely in production."""


def resolve_origins(settings: Settings) -> tuple[list[str], str | None]:
    origins = list(settings.ALLOWED_ORIGINS)
    regex = settings.ALLOWED_ORIGIN_REGEX

    if settings.DEBUG:
        for origin in _DEV_ORIGINS:
            if origin not in origins:
                origins.append(origin)
        return origins, regex

    if not origins and not regex:
        raise CORSConfigurationError(
            "ALLOWED_ORIGINS is empty and ALLOWED_ORIGIN_REGEX is not set. "
            "Set at least one of them in the environment to enable browser clients."
        )
    return origins, regex


def configure_cors(app: FastAPI, settings: Settings) -> None:
    origins, regex = resolve_origins(settings)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_origin_regex=regex,
        allow_credentials=True,
        allow_methods=list(_ALLOWED_METHODS),
        allow_headers=list(_ALLOWED_HEADERS),
        expose_headers=["Content-Length", "Content-Type"],
        max_age=_PREFLIGHT_MAX_AGE_SECONDS,
    )
