import boto3.session
import httpx
from dependency_injector import containers, providers

from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.backend.leaderboard.containers.di import LeaderboardContainer
from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.backend.settings import Settings
from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.shared_kernel.infra.database.sqla.container.di import SqlaContainer


def http_client(retries: int = 3):
    transports = httpx.AsyncHTTPTransport(retries=retries)
    client = httpx.AsyncClient(transport=transports)
    return client


class TetrowebContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[],
        modules=[
            "{{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.shared_kernel.infra.object_storage.s3",
            "{{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.shared_kernel.infra.database.sqla.mixin",
            "{{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.backend.leaderboard.rest.fastapi",
        ],
    )

    settings = providers.Resource(Settings)  # type: ignore
    boto_session = providers.Resource(boto3.session.Session, region_name="ap-northeast-2")
    s3_client = providers.Resource(
        providers.MethodCaller(boto_session.provided.client),
        service_name="s3",
    )
    sns_client = providers.Resource(
        providers.MethodCaller(boto_session.provided.client),
        service_name="sns",
    )
    database = providers.Container(SqlaContainer, settings=settings.provided.db)
    leaderboard = providers.Container(LeaderboardContainer, settings=settings)

    async_http_client = providers.Singleton(http_client)
