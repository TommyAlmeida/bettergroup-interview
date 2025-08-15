from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import get_settings


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if request.url.path in ["/docs", "/openapi.json", "/health", "/redoc"]:
            return await call_next(request)

        api_key = request.headers.get("X-API-Key")

        if not api_key or api_key != get_settings().api_key:
            return Response(
                content='{"detail": "Invalid or missing API key"}',
                status_code=401,
                media_type="application/json"
            )

        return await call_next(request)
