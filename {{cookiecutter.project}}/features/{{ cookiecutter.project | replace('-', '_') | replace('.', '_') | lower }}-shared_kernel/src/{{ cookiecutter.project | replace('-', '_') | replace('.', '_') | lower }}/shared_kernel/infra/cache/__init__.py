import logging
from typing import TYPE_CHECKING

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from . import key_builders

if TYPE_CHECKING:
    from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.shared_kernel.infra.settings.model import CacheSettings
logger = logging.getLogger("uvicorn.access")


def setting_cache(app: FastAPI, setting: "CacheSettings"):
    backend = InMemoryBackend()
    if setting.backend_url:
        logger.info("*** Using Redis cache backend ***")
        redis = aioredis.from_url(setting.backend_url)
        backend = RedisBackend(redis)
    logger.info(f"*** Key prefix: {setting.prefix} ***")
    logger.info(f"*** Expire: {setting.expire} ***")
    logger.info(f"*** Enable: {setting.enable} ***")

    FastAPICache.init(
        backend=backend,
        prefix=setting.prefix,
        expire=setting.expire,
        enable=setting.enable,
        key_builder=key_builders.request_key_builder,
    )
    return app


__all__ = ["setting_cache"]
