from fastapi import Request
from fastapi.responses import JSONResponse
from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.shared_kernel.domain.exception import BaseMsgException

from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.shared_kernel.infra.fastapi.dtos.response import ResponseDto


async def custom_exception_handler(request: Request, exe: BaseMsgException):
    return JSONResponse(
        status_code=exe.code,
        content=ResponseDto(
            status=exe.code,
            message=exe.message,
            data={
                "method": request.method,
                "path": request.url.path,
                "request_id": request.state.correlation_id,
                "detail": exe.message,
                "error": exe.error,
                "status_code": exe.code,
            },
        ),
    )
