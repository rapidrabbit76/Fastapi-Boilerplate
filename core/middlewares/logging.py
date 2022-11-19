import time
from loguru import logger
from fastapi import Request, Response
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.responses import StreamingResponse

# from loguru import logger


from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

# from loguru import logger
from core.logger  import logger




class RequestParser:
    def __call__(self, request: Request,response:Response):
        headers = request.headers
        path_params = dict(request.path_params)
        query_params = dict(request.query_params)
        msg = {
            "status_code" : response.status_code,
            "method": request.method,
            "client": request.client.host,
            "user-agent": headers['user-agent'],
            "path_params": path_params,
            "query_params": query_params,
            "process_time": response.headers.get('x-process-time',None)
        }
        return msg



class LoggingMiddleware(BaseHTTPMiddleware):
    # TODO: Body logging
    """Example logging middleware."""
    parser = RequestParser()

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        msg = self.parser(request=request,response=response)
        
        log_method = logger.info
        if 400 <= response.status_code <= 599:
            log_method = logger.error
            
        log_method(msg)
        return response
    