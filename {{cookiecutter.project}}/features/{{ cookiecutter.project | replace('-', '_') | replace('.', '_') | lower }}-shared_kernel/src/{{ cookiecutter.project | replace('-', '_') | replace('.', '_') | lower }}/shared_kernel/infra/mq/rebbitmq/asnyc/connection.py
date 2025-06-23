import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
import logging
from typing import TYPE_CHECKING
import aio_pika


if TYPE_CHECKING:
    from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.shared_kernel.infra.settings.model import RabbitMqSettings
    from aio_pika.pool import Pool as AioPikaPool


@dataclass(slots=True, kw_only=True, init=True)
class AsyncRabbitmqConnection:
    settings: "RabbitMqSettings" = field(init=True, repr=True)
    logger: logging.Logger = field(init=False, repr=False)
    connection_pool: "AioPikaPool" = field(init=False, repr=False)

    async def get_connection(self):
        settings = self.settings
        connection = await aio_pika.connect(
            settings.url,
            loop=asyncio.get_event_loop(),
            virtualhost=settings.virtualhost,
        )
        return connection

    def __post_init__(self):
        self.connection_pool = aio_pika.pool.Pool(
            self.get_connection,
            max_size=self.settings.pool_max,
            loop=asyncio.get_event_loop(),
        )

    @asynccontextmanager
    async def connection(self):
        # conn = self.connection_pool.acquire()
        conn = await self.get_connection()
        yield conn
        await conn.close()
        # await self.connection_pool.release(conn)
