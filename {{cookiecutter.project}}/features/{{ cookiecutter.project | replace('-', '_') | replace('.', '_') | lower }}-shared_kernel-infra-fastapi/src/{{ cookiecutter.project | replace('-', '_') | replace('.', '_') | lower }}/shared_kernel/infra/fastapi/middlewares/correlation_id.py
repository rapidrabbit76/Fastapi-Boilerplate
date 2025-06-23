import uuid

from starlette.middleware.base import BaseHTTPMiddleware


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        request.state.correlation_id = request.headers.get("x-correlation-id", str(uuid.uuid4()))
        response = await call_next(request)
        response.headers["x-correlation-id"] = request.state.correlation_id
        return response
