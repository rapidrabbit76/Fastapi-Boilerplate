from dataclasses import dataclass, field
from datetime import datetime

import pendulum


@dataclass(init=True)
class TimestampMixin:
    created_at: datetime = field(default_factory=datetime.utcnow, repr=False, init=False)
    updated_at: datetime = field(default_factory=datetime.utcnow, repr=False, init=False)


@dataclass(init=True)
class CreateTimestampMixin:
    created_at: datetime = field(default_factory=datetime.utcnow, repr=False)


@dataclass(init=True)
class TrashTimestampMixin(TimestampMixin):
    deleted_at: datetime = field(default_factory=datetime.utcnow, repr=False)
