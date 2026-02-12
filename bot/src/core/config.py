import os
from dotenv import load_dotenv
import pytz
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from pydantic import Field
from pydantic import field_validator
from enum import Enum

load_dotenv()

class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env" if os.getenv("DOCKER") is None else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    bot_token: str = Field(alias="BOT_TOKEN")

    database_user: str = Field(alias="DATABASE_USER")
    database_password: str = Field(alias="DATABASE_PASSWORD")
    database_host: str = Field(alias="DATABASE_HOST")
    database_port: int = Field(alias="DATABASE_PORT")
    database_name: str = Field(alias="DATABASE_NAME")

    tz: str = Field(alias="TZ")

    redis_host: str = Field(alias="REDIS_HOST")
    redis_port: int = Field(alias="REDIS_PORT")
    redis_db: int = Field(alias="REDIS_DB")

    scheduler_lock_key: str = Field(alias="SCHEDULER_LOCK_KEY")
    redis_stream_key: str = Field(alias="REDIS_STREAM_KEY")

    shop_secret_key: str = Field(alias="SHOP_SECRET_KEY")
    shop_id: str = Field(alias="SHOP_ID")

    default_smart_wallet_price: float = Field(alias="DEFAULT_SMART_WALLET_PRICE")

    app_env: Environment = Field(default=Environment.DEVELOPMENT, alias="APP_ENV")

    @property
    def is_dev(self) -> bool:
        return self.app_env == Environment.DEVELOPMENT

    @property
    def timezone(self):
        return pytz.timezone(self.tz)

settings = Settings()

# config = {
#     'BOT_TOKEN' : os.getenv('BOT_TOKEN'),
#
#     'DATABASE_USER' : os.getenv('DATABASE_USER'),
#     'DATABASE_PASSWORD' : os.getenv('DATABASE_PASSWORD'),
#     'DATABASE_HOST' : os.getenv('DATABASE_HOST'),
#     'DATABASE_PORT' : os.getenv('DATABASE_PORT'),
#     'DATABASE_NAME' : os.getenv('DATABASE_NAME'),
#
#     'TIMEZONE' : pytz.timezone(os.getenv('TZ')),
#
#     'REDIS' : {
#         'HOST': os.getenv('REDIS_HOST'),
#         'PORT': os.getenv('REDIS_PORT'),
#         'DB': os.getenv('REDIS_DB'),
#     },
#
#     'SCHEDULER_LOCK_KEY' : os.getenv('SCHEDULER_LOCK_KEY'),
#
#     'REDIS_STREAM_KEY' : os.getenv('REDIS_STREAM_KEY'),
#
#     'DEV_MODE' : os.getenv('DEV_MODE') == 'TRUE',
#
#     'SHOP_SECRET_KEY' : os.getenv('SHOP_SECRET_KEY'),
#     'SHOP_ID': os.getenv('SHOP_ID'),
# }

TORTOISE_ORM = {
    'connections': {
            'default': f"asyncpg://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}",
        },
    'apps': {
        'models': {
            'models': ['src.models'],
            'default_connection': 'default',
        }
    },
    'use_tz': True,
    'timezone': 'UTC',
}

