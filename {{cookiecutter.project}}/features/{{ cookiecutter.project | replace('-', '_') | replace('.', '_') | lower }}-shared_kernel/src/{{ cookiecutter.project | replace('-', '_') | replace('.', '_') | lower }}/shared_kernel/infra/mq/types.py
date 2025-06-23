from datetime import datetime
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class WorkerStateType(StrEnum):
    PENDING = "pending"
    START = "start"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkerStatus(BaseModel):
    state: WorkerStateType = Field(default=WorkerStateType.PENDING)
    message: str | None = Field(default=None)
    progress: Optional[float] = Field(default=None, ge=0, le=100)


class WorkerCallback(BaseModel):
    class CallbackType(StrEnum):
        HTTP = "http"
        LAMBDA = "lambda"

    type: str = Field(default=CallbackType.HTTP)
    is_async: bool = Field(default=False)
    target_state: WorkerStateType = Field(default=WorkerStateType.COMPLETED)
    target: str | None = None
    url: str | None = None
    body: dict | None = None
    header: dict | None = None
    timeout: int | None = None


class WorkerPayload(BaseModel):
    id: str
    status: WorkerStatus = Field(default_factory=WorkerStatus)
    payload: Any
    results: Any | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    callbacks: list[WorkerCallback] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
