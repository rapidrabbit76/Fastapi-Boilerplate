from contextvars import ContextVar, Token
from typing import Union

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql.expression import Update, Delete, Insert

from core.settings import env


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
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return engines["writer"].sync_engine
        else:
            return engines["reader"].sync_engine


async_session_factory = sessionmaker(
    class_=AsyncSession,
    sync_session_class=RoutingSession,
)


async def get_db_session() -> AsyncSession:
    session = async_session_factory()
    try:
        yield session
    finally:
        await session.close()


session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_session_context,
)


Base = declarative_base()
