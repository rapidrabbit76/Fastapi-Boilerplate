from contextlib import asynccontextmanager
from fastapi.applications import FastAPI


@asynccontextmanager
async def lifespan(app: "FastAPI"):
    # Run migration
    try:
        yield
    except Exception as e:
        raise e
    finally:
        ...
