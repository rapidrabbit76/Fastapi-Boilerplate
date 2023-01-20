from contextvars import ContextVar, Token
from typing import Union

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql.expression import Update, Delete, Insert

from core.settings import env
from starlette.requests import Request


session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


engines = {
    "writer": create_async_engine(
        env.DB_WRITER_DB_URL,
        pool_recycle=env.DB_POOL_RECYCLE,
        echo=env.DB_ECHO,
    ),
    "reader": create_async_engine(
        env.DB_READER_DB_URL,
        pool_recycle=env.DB_POOL_RECYCLE,
        echo=env.DB_ECHO,
    ),
}


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        bind_key = "reader"
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return engines["writer"].sync_engine

        if hasattr(mapper.class_, "__bind_key__"):
            bind_key = mapper.class_.__bind_key__
            return engines[bind_key].sync_engine

        return engines["reader"].sync_engine


async_session_factory = sessionmaker(
    class_=AsyncSession,
    sync_session_class=RoutingSession,
)


def get_db_session(request: Request):
    return request.state.db


Base = declarative_base()
