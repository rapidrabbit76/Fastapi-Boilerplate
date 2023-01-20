from typing import List, Optional
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    exception_path: List[str] = [
        "/",
        "/health",
        "/docs",
        "/openapi.json",
        "/favicon.ico",
    ]

    def __init__(
        self,
        app,
        logger_name: Optional[str] = None,
        exception_path: List[str] = [
            "/",
            "/health",
            "/docs",
            "/openapi.json",
            "/favicon.ico",
        ],
    ):
        super().__init__(app)
        self.logger = logging.getLogger(name=logger_name)
        self.exception_path = exception_path

    def is_in_exception_path(self, request: Request) -> bool:
        return request.url.path in self.exception_path

    async def dispatch(self, request, call_next):
        logging_flag = not self.is_in_exception_path(request=request)
        req_uuid = request.state.correlation_id

        self.logger.info(
            "request",
            extra={
                "uuid": req_uuid,
                "type": "api-request",
                "client": {
                    "host": request.client.host,
                    "user-agent": request.headers["user-agent"],
                },
                "method": str(request.method).upper(),
                "path": request.url.path,
            },
        )

        ######################################################################
        response = await call_next(request)
        ######################################################################

        if logging_flag:
            self.logger.info(
                "response",
                extra={
                    "uuid": req_uuid,
                    "type": "api-response",
                    "code": response.status_code,
                },
            )
        return response
