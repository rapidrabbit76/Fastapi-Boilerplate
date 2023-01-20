from fastapi import FastAPI


import api


from core.middlewares import (
    Middleware,
    CORSMiddleware,
    GZipMiddleware,
    CorrelationIdMiddleware,
    LoggingMiddleware,
    SQLAlchemyMiddleware,
)
from core.exceptions import (
    HTTPException,
    exception_handler,
    http_exception_handler,
)
from core import events
from core.logger import configure_logging
from core.settings import env

configure_logging(
    logging_path=env.LOG_PATH,
    logging_filename=env.LOG_FILENAME,
    service="Backend",
)


def create_app() -> FastAPI:
    app = FastAPI(
        redoc_url=None,
        docs_url=None if env.MODE.upper() == "PROD" else "/docs",
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=env.CORS_ALLOW_ORIGINS,
                allow_credentials=env.CORS_CREDENTIALS,
                allow_methods=env.CORS_ALLOW_METHODS,
                allow_headers=env.CORS_ALLOW_HEADERS,
            ),
            Middleware(
                SQLAlchemyMiddleware,
            ),
            Middleware(CorrelationIdMiddleware),
            Middleware(LoggingMiddleware),
            Middleware(
                GZipMiddleware,
                minimum_size=env.GZIP_MININUM_SIZE,
                compresslevel=env.GZIP_COMPRESS_LEVEL,
            ),
        ],
        exception_handlers={
            Exception: exception_handler,
            HTTPException: http_exception_handler,
        },
    )
    app.include_router(api.router)
    return app


app = create_app()
app.add_event_handler("startup", events.startup_event)
