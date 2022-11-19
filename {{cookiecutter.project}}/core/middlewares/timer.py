import time
from fastapi import Request, Response
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from fastapi.middleware.trustedhost import TrustedHostMiddleware


class TimeHeaderMiddleware(BaseHTTPMiddleware):
    """Example logging middleware."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = f"{process_time :.4f}"
        return response
