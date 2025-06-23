from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.shared_kernel.infra.database.sqla import Base
from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.shared_kernel.infra.database.sqla.mixin import TimestampMixin


class LeaderBoardLog(Base, TimestampMixin):
    __tablename__ = "{{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}_leaderboard_log"
    # extend_existing=True
    __table_args__ = (
        sa.Index(
            f"idx_{__tablename__}_user_id_game_date",
            "user_id",
            "game",
            "created_at",
            unique=True,
        ),
    )

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(sa.String(48), nullable=False)
    game: Mapped[str] = mapped_column(sa.String(10), nullable=False)
    score: Mapped[int] = mapped_column(sa.Integer, nullable=False, default=0)
    name: Mapped[str] = mapped_column(sa.Text, nullable=False)
    email: Mapped[str] = mapped_column(sa.Text, nullable=True, default=None)

    created_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP(timezone=True), default=sa.func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP(timezone=True), nullable=False, default=sa.func.now(), onupdate=sa.func.now()
    )
