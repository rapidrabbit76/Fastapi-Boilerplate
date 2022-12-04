import typing as T
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

import api

from core.exceptions.base import CustomException
from core.middlewares.authentication import (
    AuthBackend,
    AuthenticationMiddleware,
    on_auth_error,
)
from core.middlewares.logging import LoggingMiddleware
from core.middlewares.sqlalchemy import SQLAlchemyMiddleware
from core.middlewares.timer import TimeHeaderMiddleware
from core.middlewares.cache_control import CacheControl, CacheControlMiddleware
from core.settings import env

from core.admin import admin_app


def init_router(app: FastAPI):
    app.include_router(api.home.router, tags=["Home"])


def create_app() -> FastAPI:
    app = FastAPI(
        redoc_url=None,
        title=env.TITLE,
        description=env.DESCRIPTION,
        middleware=init_middleware(),
    )
    init_settings(app)
    init_router(app)
    admin_app(app)

    return app


def init_middleware() -> T.List[Middleware]:
    middlewares = [
        Middleware(
            CORSMiddleware,
            allow_origins=env.CORS_ALLOW_ORIGINS,
            allow_credentials=env.CORS_CREDENTIALS,
            allow_methods=env.CORS_ALLOW_METHODS,
            allow_headers=env.CORS_ALLOW_HEADERS,
        ),
        # SQLAlchemy session Middleware
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        # SQLAlchemy session Middleware
        Middleware(SQLAlchemyMiddleware),
        # Req logging Middleware
        Middleware(LoggingMiddleware),
        # Time Header Middleware
        Middleware(TimeHeaderMiddleware),
        # Cahce-Control Middleware
        Middleware(
            CacheControlMiddleware,
            cache_control=CacheControl(
                cacheablity=env.CACHE_CONTROL_CACHEABLITY,
                max_age=env.CACHE_CONTROL_MAX_AGE,
                s_maxage=env.CACHE_CONTROL_S_MAXAGE,
            ),
        ),
    ]

    if env.GZIP_ENABLE:
        middlewares.append(
            Middleware(
                GZipMiddleware,
                minimum_size=env.GZIP_MININUM_SIZE,
                compresslevel=env.GZIP_COMPRESS_LEVEL,
            )
        )
    return middlewares


def init_settings(app: FastAPI):
    @app.on_event("startup")
    async def startup_event():
        if env.DB_INIT:
            from core.db.session import Base, engines

            async with engines["writer"].begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

    @app.on_event("shutdown")
    def shutdown_event():
        pass

    @app.exception_handler(CustomException)
    async def custom_exception_handler(
        request: Request,
        exc: CustomException,
    ):
        return JSONResponse(
            status_code=exc.code,
            content={
                "error_code": exc.error_code,
                "message": exc.message,
            },
        )


app = create_app()
