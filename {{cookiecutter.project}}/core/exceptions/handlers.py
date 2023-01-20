import logging
import traceback
import sys
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

logger = logging.getLogger()


async def exception_handler(request: Request, exc: Exception):
    type, value, tb = sys.exc_info()
    ex_traceback = traceback.format_exception(type, value, tb)
    logger.exception(
        exc,
        extra={
            "uuid": request.state.correlation_id,
            "type": "app-error",
            "call_stack": ex_traceback,
        },
    )
    return JSONResponse(
        status_code=500,
        content={
            "uuid": request.state.correlation_id,
            "message": "An internal error has occurred",
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    type, value, tb = sys.exc_info()
    ex_traceback = traceback.format_exception(type, value, tb)
    logger.exception(
        exc,
        extra={
            "uuid": request.state.correlation_id,
            "type": "api-error",
            "call_stack": ex_traceback,
        },
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "uuid": request.state.correlation_id,
            "message": exc.detail,
        },
    )
