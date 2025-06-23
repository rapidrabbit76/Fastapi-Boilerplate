import hashlib
from typing import Callable, Optional
from fastapi import Request, Response
from fastapi_cache import FastAPICache


def request_key_builder(
    func,
    namespace: str = "",
    *,
    request: Request = None,
    response: Response = None,
    **kwargs,
):
    params = str(request.query_params)
    cache_key = ":".join(
        [
            FastAPICache.get_prefix(),
            namespace,
            request.method.lower(),
            request.url.path,
            hashlib.md5(params.encode()).hexdigest(),
        ]
    )
    return cache_key


def default_key_builder(
    func: Callable,
    namespace: Optional[str] = "",
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
) -> str:
    if "self" in kwargs:
        kwargs["self"].pop()
    prefix = f"{FastAPICache.get_prefix()}:{namespace}:"
    cache_key = prefix + hashlib.md5(f"{func.__module__}:{func.__name__}:{args}:{kwargs}".encode()).hexdigest()
    return cache_key
