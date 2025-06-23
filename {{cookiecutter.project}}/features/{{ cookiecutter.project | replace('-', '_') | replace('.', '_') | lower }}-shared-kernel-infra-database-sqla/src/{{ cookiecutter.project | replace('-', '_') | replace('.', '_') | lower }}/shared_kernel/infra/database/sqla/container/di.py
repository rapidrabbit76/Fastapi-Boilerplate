from dependency_injector import containers, providers

from ..connection import SyncDatabase
from ..settings import DatabaseSettings


class SqlaContainer(containers.DeclarativeContainer):
    settings = providers.Resource(DatabaseSettings)  # type: ignore
    db = providers.Singleton(SyncDatabase, settings=settings)
