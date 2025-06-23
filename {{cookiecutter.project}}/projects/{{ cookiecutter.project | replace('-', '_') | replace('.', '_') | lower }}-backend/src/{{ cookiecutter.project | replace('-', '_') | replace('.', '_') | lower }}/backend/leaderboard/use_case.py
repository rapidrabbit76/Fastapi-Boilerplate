from dataclasses import dataclass
from typing import TYPE_CHECKING

import sqlalchemy as sa

from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.backend.leaderboard.dtos.schemas import LreaderBoardReadSchema
from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.backend.leaderboard.entities.leaderboard import LeaderBoardLog
from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.shared_kernel.infra.database.sqla.mixin import SyncSqlaMixIn


if TYPE_CHECKING:
    from .dtos.request import CreateLeaderBoardRequest


@dataclass
class LeaderboardUseCase(SyncSqlaMixIn):
    def summit_score(
        self,
        payload: "CreateLeaderBoardRequest",
    ) -> LeaderBoardLog:
        with self.db.session() as session:
            log = LeaderBoardLog(
                user_id=payload.user_id, game=payload.game, score=payload.score, name=payload.name, email=payload.email
            )
            session.add(log)
            session.commit()
        return log

    async def get_leader_board_by_game(self, game: str, topk: int = 100) -> list[LreaderBoardReadSchema]:
        with self.db.session() as session:
            stmt = sa.select(
                LeaderBoardLog.id,
                LeaderBoardLog.user_id,
                sa.func.max(LeaderBoardLog.score).label("score"),
                LeaderBoardLog.name,
                LeaderBoardLog.email,
                LeaderBoardLog.created_at,
            ).where(LeaderBoardLog.game == game)
            stmt = stmt.order_by(sa.desc("score")).limit(topk)
            stmt = stmt.group_by(LeaderBoardLog.user_id)
            results = session.execute(stmt).all()
        results = [
            LreaderBoardReadSchema(id=id, user_id=user_id, score=score, name=name, email=email, created_at=created_at)
            for id, user_id, score, name, email, created_at in results
        ]
        return results
