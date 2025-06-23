from typing import Any

from fastapi import Response
from simplexml import dumps
from starlette.responses import JSONResponse as JSONResponse  # noqa
from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.shared_kernel.infra.camel_model import CamelModel

try:
    import msgspec
except ImportError:  # pragma: nocover
    msgspec = None  # type: ignore


class MsgSpecJSONResponse(JSONResponse):
    """
    JSON response using the high-performance ujson library to serialize data to JSON.
    """

    def render(self, content: Any) -> bytes:
        assert msgspec is not None, "msgpack must be installed to use MsgSpecJSONResponse"
        return msgspec.json.encode(content)


class XmlResponse(Response):
    media_type = "text/xml"

    def render(self, content: Any) -> bytes:
        return dumps({"response": content}).encode("utf-8")


class ExceptionResponse(CamelModel):
    request_id: str
    detail: str
    error: str
    status_code: int
