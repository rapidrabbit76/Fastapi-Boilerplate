from __future__ import annotations
from starlette.middleware.sessions import SessionMiddleware  # noqa: F401

from fastapi import Request
from .model import SessionModel


class AppSessionManager:
    request: Request

    @classmethod
    def get_session(cls, request: Request) -> AppSessionManager:
        manager = cls()
        manager.request = request
        return manager

    @property
    def session(self) -> None | SessionModel:
        return SessionModel.model_validate(self.request.session)

    @session.setter
    def session(self, session: SessionModel | dict) -> None:
        if isinstance(session, SessionModel):
            session = session.model_dump()

        self.request.session.update(session)

    def clear(self) -> None:
        self.request.session.clear()
