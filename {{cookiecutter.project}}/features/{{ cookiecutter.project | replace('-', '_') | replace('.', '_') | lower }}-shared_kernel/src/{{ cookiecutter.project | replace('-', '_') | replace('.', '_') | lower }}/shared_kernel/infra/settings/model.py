import typing as T
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class DatabaseSettings(BaseModel):
    url: str = Field("", description="Database URL", init=False)
    init: bool = False
    echo: bool = True
    pool_size: int = 10
    max_overflow: int = 2
    pool_recycle: int = 3600
    pg_schema: str = "public"
    pool_timeout: int = 30
    pool_recycle: int = 1800
    pool_pre_ping: bool = True

    def dict(self):
        return {
            "url": self.url,
            "echo": self.echo,
            "max_overflow": self.max_overflow,
        }


class AWSSettings(BaseModel):
    region: str = "us-east-1"
    endpoint_url: str | None = None


class LoggerSettings(BaseModel):
    path: str = "logs"
    filename: str = "access.json"
    level: str = "info"
    rotation: str = "1 days"
    retention: str = "1 months"


class CacheSettings(BaseModel):
    backend_url: str | None = None
    expire: int = 30
    prefix: str = ""
    enable: bool = True


class JWTSettings(BaseModel):
    secret_key: str = "SECRET"
    algorithm: str = "HS256"
    refresh_token_exp: int = 31_536_000
    access_token_exp: int = 31_536_000


class AuthManagerSettings(BaseModel):
    secret_key: str = "SECRET"
    lifetime_seconds: int = 300


class OAuthSettings(BaseModel):
    client_id: str = ""
    client_secrets: str = ""
    redirect_url: str | None = None


class AuthSettings(BaseModel):
    cookie_max_age: int = 3600
    cookie_name: str = "x-auth-designovel-sass"
    cookie_domain: str | None = None
    state_secret: str = "sample"


class GZipSettings(BaseModel):
    enable: bool = True
    mininum_size: int = 800
    compress_level: int = 9

    @field_validator("compress_level")
    def check_compress_level_rate(cls, v):
        if not (0 <= v <= 9):
            raise ValueError(f"GZIP_COMPRESS_LEVEL Range ERR,{v} is not in 0~9")
        return v


class CORSSettings(BaseModel):
    allow_origins: T.List[str] = [
        "*",
        "http://localhost:3000",
        "http://localhost:8000",
        "https://app.{{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.ai",
    ]
    allow_credentials: bool = True
    allow_methods: T.List[str] = ["*"]
    allow_headers: T.List[str] = ["*"]


class SessionSettings(BaseModel):
    secret_key: str = "1q2w3e4r"


class RedisStoreSettings(BaseModel):
    url: str = ""
    lifetime_seconds: int = 31536000


class AuthCookieSettings(BaseModel):
    name: str = "x-auth-lexicon-harvesting"
    domain: str | None = None
    samesite: T.Literal["lax", "strict", "none"] = "none"


class EmailSettings(BaseModel):
    sender: str = "no-reply@designovel.com"
    domain_url: str = "https://app.{{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.ai"
    reset_password_path: str = "reset-password"
    invite_path: str = "auth/callback/org/invite"
    verify_path: str = "auth/callback/verify"


class JinaHttpSettings(BaseModel):
    url: str = "http://localhost:8000"
    timeout: int = 60
    target_executor: str
    exec_endpoint: str


class RatelimiterSettings(BaseModel):
    key_func: str = "get_remote_address"
    key_prefix: str = ""
    enabled: bool = True
    storage_uri: str | None = None
    strategy: str = "moving-window"


class ObjectStorageSettings(BaseModel):
    buket: str = "designovel"
    prefix_key: str | None = None


class SentrySettings(BaseModel):
    dsn: str = ""
    traces_sample_rate: float = 1.0
    profiles_sample_rate: float = 1.0
    environment: str = "test"


class CookieSettings(BaseModel):
    key: str = ""
    domain: str | None = None
    samesite: T.Literal["lax", "strict", "none"] = "lax"
    httponly: bool = True
    path: str = "/"
    secure: bool = True
    max_age: int | None = None
    expires: datetime | str | int | None = None


class FastAPISettings(BaseModel):
    title: str = "FastAPI"
    description: str = "FastAPI"
    docs_url: str | None = None
    redoc_url: str | None = None
    openapi_url: str = "/openapi.json"
    contact: dict = {
        "name": "yslee(rapidrabbit76)",
        "email": "yslee.dev@gmail.com",
    }
    summary: str = "Designovel SaaS API"


class RedisSettings(BaseModel):
    url: str = ""


class RabbitMqSettings(BaseModel):
    url: str = Field(default="amqp://guest:guest@localhost:5672/")
    virtualhost: str = Field(default="/")
    pool_max: int = Field(default=10)
    pool_min: int = Field(default=2)


class S3UploadSettings(BaseModel):
    bucket_name: str = "designovel"
    dir_name: str = "images/ml/gen"
    cdn_url: str = "https://cdn.designovel.com"


class PrometheusSettings(BaseModel):
    secret: str = "secret"
    should_gzip: bool = True
    endpoint: str = "/metrics"
    include_in_schema: bool = False
    namespace: str = "designovel.saas.backend.production"
    metric_subsystem: str = ""


class TossPaymentGatewaySettings(BaseModel):
    secret_key: str = ""
    client_key: str = ""


class OpenWebUISettings(BaseModel):
    url: str = "https://chat.idc.designovel.com"
    admin_token: str = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjBiZmQ4OGZjLWQ3YzktNGQ4ZC04OGRiLWEzYjY4NDU5YmUwYSJ9.HpkIhpRtmXByL9LpaFLsO20UvP8wd3Yvqzo8FJ23mtU"


class NaverShoppingAPISettings(BaseModel):
    api_key: str = (
        "01000000004af83b044b8ae13752e404c037b55b03336cf489b7254d445b7261ca00ff5b1b"
    )
    secret_key: str = "AQAAAABK+DsES4rhN1LkBMA3tVsDQPM73aT63PgjxDj5zl4pEw=="
    customer_id: str = "2196173"


class OpenAISettings(BaseModel):
    api_key: str
