import os
import typing as T
from pydantic import BaseSettings, validator


class DatabaseSetting(BaseSettings):
    DB_WRITER_DB_URL: str = "mysql+aiomysql://admin:admin@localhost:3306/mydatabase"
    DB_READER_DB_URL: str = "mysql+aiomysql://admin:admin@localhost:3306/mydatabase"
    DB_INIT: bool = False
    DB_POOL_RECYCLE: int = 3600
    DB_ECHO: bool = False


class LoggerSettings(BaseSettings):
    LOG_PATH: str = "logs"
    LOG_FILENAME: str = "access.json"
    LOG_LEVEL: str = "info"
    LOG_ROTATION: str = "1 days"
    LOG_RETENTION: str = "1 months"


class SecuritySetting(BaseSettings):
    JWT_SECRET_KEY: str = "SECRET"
    JWT_ALGORITHM: str = "HS256"
    JWT_REFRESH_TOKEN_EXP: int = 1_209_600
    JWT_ACCESS_TOKEN_EXP: int = 3600


class CacheSetting(BaseSettings):
    CACHE_CONFIG_FILE_PATH: str = "env/cache.yaml"
    CACHE_ALIAS: str = "local"
    CACHE_REDIS_HOST: str = "localhost"
    CACHE_REDIS_PORT: int = 6379

    @validator("CACHE_CONFIG_FILE_PATH")
    def is_cache_config_file_exists(cls, v):
        if not os.path.exists(v):
            raise FileNotFoundError(f"{v} is not exists")
        return v


class CacheControlSetting(BaseSettings):
    CACHE_CONTROL_ENABLE: bool = True
    CACHE_CONTROL_MAX_AGE: int = 10
    CACHE_CONTROL_S_MAXAGE: int = None
    CACHE_CONTROL_CACHEABLITY: str = "public"

    @validator("CACHE_CONTROL_MAX_AGE", "CACHE_CONTROL_S_MAXAGE")
    def check_range(cls, v):
        if v is None:
            return v

        if v < 0:
            raise ValueError(
                f" Cache-Control max-age is biger then 0, {v} is not Accepted"
            )
        return v


class GZipSetting(BaseSettings):
    GZIP_ENABLE: bool = True
    GZIP_MININUM_SIZE: int = 800
    GZIP_COMPRESS_LEVEL: int = 9

    @validator("GZIP_COMPRESS_LEVEL")
    def check_compress_level_rate(cls, v):
        if not (0 <= v <= 9):
            raise ValueError(f"GZIP_COMPRESS_LEVEL Range ERR,{v} is not in 0~9")
        return v


class MiddleWareSetting(BaseSettings):
    TIME_HEADER_ENABLE: bool = True
    LOGGING_ENABLE: bool = True


class Settings(
    DatabaseSetting,
    LoggerSettings,
    CacheSetting,
    SecuritySetting,
    CacheControlSetting,
    GZipSetting,
    MiddleWareSetting,
):
    CORS_ALLOW_ORIGINS: T.List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: T.List[str] = ["*"]
    CORS_ALLOW_HEADERS: T.List[str] = ["*"]

    MODE: str = "DEV"

    TITLE: str = "{{cookiecutter.project}}"
    DESCRIPTION: str = "{{cookiecutter.description}}"
    
    TITLE: str = ""
    DESCRIPTION: str = ""
