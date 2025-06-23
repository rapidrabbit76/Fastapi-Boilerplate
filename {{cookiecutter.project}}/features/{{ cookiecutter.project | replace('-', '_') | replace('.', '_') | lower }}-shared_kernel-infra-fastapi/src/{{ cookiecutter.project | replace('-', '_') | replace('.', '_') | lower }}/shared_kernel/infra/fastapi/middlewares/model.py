from __future__ import annotations
from pydantic import BaseModel


class SessionModel(BaseModel):
    version: str | None
    current_time: str | None
