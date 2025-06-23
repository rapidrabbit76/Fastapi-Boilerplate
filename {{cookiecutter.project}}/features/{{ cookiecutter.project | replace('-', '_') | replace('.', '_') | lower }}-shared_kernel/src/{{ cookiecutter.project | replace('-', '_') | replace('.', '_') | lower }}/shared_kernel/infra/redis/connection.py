from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass, field
import logging
import redis.asyncio as aioredis
from redis import Redis
import redis


@dataclass(slots=True, kw_only=True, init=True)
class AsyncRedisConnection:
    url: str = field(init=True, repr=True)
    logger: logging.Logger = field(init=False, repr=False)
    pool: aioredis.ConnectionPool = field(init=False, repr=False)
    redis: aioredis.Redis = field(init=False, repr=False)
    max_connections: int = field(default=5, init=True, repr=True)
    health_check_interval: int = field(default=30, init=True, repr=True)

    def __post_init__(self):
        self.pool = aioredis.ConnectionPool.from_url(
            self.url,
            max_connections=self.max_connections,
            health_check_interval=self.health_check_interval,
        )
        self.redis = aioredis.Redis.from_pool(self.pool)
        self.logger = logging.getLogger(self.__class__.__name__)

    @asynccontextmanager
    async def session(self):
        try:
            yield self.redis
        except Exception as e:
            self.logger.error(e)
            raise e
        finally:
            pass

    async def close(self):
        self.logger.info("Closing Redis connection pool...")
        await self.pool.disconnect(inuse_connections=True)


@dataclass(slots=True, kw_only=True, init=True)
class RedisConnection:
    url: str = field(init=True, repr=True)
    logger: logging.Logger = field(init=False, repr=False)
    pool: redis.ConnectionPool = field(init=False, repr=False)

    def __post_init__(self):
        self.pool = redis.ConnectionPool.from_url(self.url)
        self.logger = logging.getLogger(self.__class__.__name__)

    @contextmanager
    def session(self):
        connection = Redis(connection_pool=self.pool)
        try:
            yield connection
        except Exception as e:
            raise e
        finally:
            connection.close()
