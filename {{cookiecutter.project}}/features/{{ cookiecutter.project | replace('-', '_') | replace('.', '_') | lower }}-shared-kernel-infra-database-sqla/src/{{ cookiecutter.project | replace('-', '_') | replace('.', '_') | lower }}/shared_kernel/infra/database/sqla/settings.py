import typing as T
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class DatabaseSettings(BaseModel):
    url: str = Field("", description="Database URL", init=False)
    init: bool = False
    echo: bool = True
    pool_size: int = 10
    max_overflow: int = 2
    pool_recycle: int = 3600
    pg_schema: str = "public"
    pool_timeout: int = 30
    pool_recycle: int = 1800
    pool_pre_ping: bool = True

    def dict(self):
        return {
            "url": self.url,
            "echo": self.echo,
            "max_overflow": self.max_overflow,
        }
