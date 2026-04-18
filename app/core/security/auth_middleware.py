from __future__ import annotations

from typing import Iterable

from fastapi import Request
from fastapi.responses import JSONResponse
from jose import JWTError, jwt

from app.core.config import settings


def _is_public_path(path: str, public_paths: Iterable[str], public_prefixes: Iterable[str]) -> bool:
    if path in public_paths:
        return True
    for prefix in public_prefixes:
        if path.startswith(prefix):
            return True
    return False


async def auth_middleware(request: Request, call_next):
    public_paths = (
        "/",  # home
        "/openapi.json",
    )
    public_prefixes = (
        "/docs",
        "/redoc",
        "/login",
        "/register",
        "/google",
    )

    if _is_public_path(request.url.path, public_paths, public_prefixes):
        return await call_next(request)

    auth_header = request.headers.get("authorization")
    if not auth_header:
        return JSONResponse(status_code=401, content={"detail": "Missing Authorization header"})

    scheme, _, token = auth_header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return JSONResponse(status_code=401, content={"detail": "Invalid Authorization header"})

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except JWTError:
        return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

    request.state.user = payload
    return await call_next(request)

