from datetime import datetime
from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.shared_kernel.infra.camel_model import CamelModel


class LeaderBoardSchema(CamelModel):
    id: int | None = None
    user_id: str
    game: str
    score: int
    name: str
    email: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class LreaderBoardReadSchema(CamelModel):
    id: int
    user_id: str
    score: int
    name: str
    email: str | None = None
    created_at: datetime | None = None
