from fastapi.exceptions import (
    FastAPIError,
    HTTPException,
    RequestErrorModel,
    WebSocketErrorModel,
)
from fastapi import status as http_status
from .handlers import http_exception_handler, exception_handler


class CustomHTTPException(HTTPException):
    status_code = http_status.HTTP_400_BAD_REQUEST
    detail = ""
    headers = None

    def __init__(
        self,
        status_code=None,
        detail=None,
        headers=None,
    ) -> None:
        if status_code is None:
            status_code = self.status_code
        if detail is None:
            detail = self.detail
        if headers is None:
            headers = self.headers
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers,
        )


__all__ = [
    "http_status",
    "CustomHTTPException",
    "HTTPException",
    "FastAPIError",
    "RequestErrorModel",
    "WebSocketErrorModel",
    "http_exception_handler",
    "exception_handler",
]
