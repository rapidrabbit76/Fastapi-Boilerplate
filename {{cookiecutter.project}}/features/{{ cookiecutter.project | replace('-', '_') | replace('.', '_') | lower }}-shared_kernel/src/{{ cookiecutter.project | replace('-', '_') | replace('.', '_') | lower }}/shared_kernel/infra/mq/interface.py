from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import logging
from typing import Any, Generic, TypeVar
import uuid


T = TypeVar("T")


@dataclass(init=True, repr=True, kw_only=True)
class IAsyncWorkerManager(ABC, Generic[T]):
    queue: str | None = field(init=True, repr=True, default=None)
    broker_connection_manager: T = field(init=False, repr=False)
    logger: logging.Logger = field(init=False, repr=False)

    def __post_init__(self):
        self.logger = logging.getLogger(
            f"{self.__class__.__name__}.{self.queue}",
        )

    @abstractmethod
    def send(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def build_id(self) -> str:
        return str(uuid.uuid4())
