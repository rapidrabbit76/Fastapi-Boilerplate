import httpx
from dataclasses import dataclass
from fastapi import Response, Request
from starlette.background import BackgroundTask
from fastapi.responses import StreamingResponse


@dataclass(init=True, kw_only=True, slots=True, frozen=True)
class AsyncHttpGatewayService:
    client: httpx.AsyncClient

    async def request(self, request: Request) -> Response | StreamingResponse:
        url = httpx.URL(path=request.url.path, query=request.url.query.encode("utf-8"))
        headers = [(k, v) for k, v in request.headers.raw if k != b"host"]
        req = self.client.build_request(method=request.method, url=url, headers=headers, content=request.stream())
        response = await self.client.send(req, stream=True)
        return StreamingResponse(
            response.aiter_raw(),
            headers=response.headers,
            status_code=response.status_code,
            background=BackgroundTask(response.aclose),
        )
