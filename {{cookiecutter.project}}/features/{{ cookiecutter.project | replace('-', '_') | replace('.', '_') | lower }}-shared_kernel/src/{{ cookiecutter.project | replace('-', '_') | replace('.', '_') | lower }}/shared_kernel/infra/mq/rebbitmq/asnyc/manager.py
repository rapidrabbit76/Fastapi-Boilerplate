from dataclasses import dataclass, field
import json
from dependency_injector.wiring import inject, Provide
from typing import Any, Optional
import uuid
import aio_pika
from pydantic import BaseModel, Field


from ...types import WorkerPayload, WorkerStatus, WorkerCallback, WorkerStateType  # noqa: F401
from .connection import AsyncRabbitmqConnection
from ...interface import IAsyncWorkerManager


from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.shared_kernel.infra.redis.connection import RedisConnection


@dataclass(init=True, kw_only=True)
class DramatiqWorkerMnager(IAsyncWorkerManager[AsyncRabbitmqConnection]):
    namespace: Optional[str] = field(init=True, repr=True, default=None)
    redis: "RedisConnection"

    class Message(BaseModel):
        message_id: str
        queue_name: str
        actor_name: str
        args: list = Field(default_factory=list)
        kwargs: dict = Field(default_factory=dict)
        options: dict = Field(default_factory=dict)

    @inject
    def __post_init__(
        self,
        connection_manager: AsyncRabbitmqConnection = Provide["rabbitmq"],
    ):
        super().__post_init__()
        self.connection_manager = connection_manager

    def build_id(self) -> str:
        if self.namespace is not None:
            return f"{self.namespace}:{uuid.uuid4()}"
        return str(uuid.uuid4())

    async def send(
        self,
        *,
        queue: str = "",
        actor: str,
        payload: dict,
        callbacks: list[WorkerCallback] | None = None,
        **kwargs,
    ) -> Any:
        assert queue != "" or queue is not self.queue
        assert isinstance(payload, dict)
        if queue == "" and self.queue is not None:
            queue = self.queue
        message_id = self.build_id()
        callbacks = callbacks if callbacks is not None else []
        message = self.Message(
            message_id=message_id,
            queue_name=queue,
            actor_name=actor,
            kwargs={"message": WorkerPayload(id=message_id, payload=payload, callbacks=callbacks)},
        )
        async with self.connection_manager.connection() as connection:
            body = message.model_dump_json(exclude_none=True).encode("utf-8")
            channel = await connection.channel()
            await channel.default_exchange.publish(routing_key=queue, message=aio_pika.Message(body=body))
        with self.redis.session() as session:
            body = json.dumps(
                {
                    "id": message_id,
                    "status": WorkerStatus().model_dump(),
                    "results": None,
                }
            )
            session.set(message_id, body)
        return message_id
