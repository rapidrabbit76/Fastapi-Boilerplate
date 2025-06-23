import logging
from dataclasses import dataclass, field
from typing import Union, TYPE_CHECKING
from contextlib import contextmanager
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
)

from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy import create_engine, Engine


from typing_extensions import Annotated

if TYPE_CHECKING:
    from .settings import DatabaseSettings

logger = logging.getLogger("{{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.database.sqla")
AsyncSessions = Annotated[
    Union[AsyncSession, async_scoped_session], "SQLA AsyncSession"
]
Sessions = Annotated[Union[Session, scoped_session], "SQLA Session"]


@dataclass(init=True, kw_only=True, slots=True)
class SyncDatabase:
    engine: Engine = field(init=False, repr=False)
    session_factory: sessionmaker = field(init=False, repr=False)
    settings: "DatabaseSettings" = field(init=True, repr=False)

    def __post_init__(self) -> None:
        url = self.settings.url
        echo = self.settings.echo

        engine = create_engine(url, echo=echo)
        self.engine = engine
        self.session_factory = sessionmaker(
            bind=engine, expire_on_commit=False, autocommit=False, autoflush=False
        )

    @contextmanager
    def session(self) -> Sessions:
        session: Sessions = self.session_factory()

        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e
        finally:
            if isinstance(session, Session):
                session.close()
            elif isinstance(session, scoped_session):
                session.remove()
        logger.info(f"pool: {self.engine.pool.status()}")
