import typing as T
from datetime import datetime

from fastapi import (
    APIRouter,
    Response,
)

from core.cache import cached
from core.settings import env

router = APIRouter()


@router.get("/")
@cached(
    ttl=5,
    alias=env.CACHE_ALIAS,
)
async def index():
    """ELB check"""
    current_time = datetime.utcnow()
    msg = (
        f"Notification API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')})"
    )
    return Response(msg)
