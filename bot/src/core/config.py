import os
from dotenv import load_dotenv
import pytz
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from pydantic import Field
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

    #DATABASE
    database_user: str = Field(alias="DATABASE_USER")
    database_password: str = Field(alias="DATABASE_PASSWORD")
    database_host: str = Field(alias="DATABASE_HOST")
    database_port: int = Field(alias="DATABASE_PORT")
    database_name: str = Field(alias="DATABASE_NAME")

    #REDIS
    redis_host: str = Field(alias="REDIS_HOST")
    redis_port: int = Field(alias="REDIS_PORT")
    redis_db: int = Field(alias="REDIS_DB")
    scheduler_lock_key: str = Field(alias="SCHEDULER_LOCK_KEY")
    redis_stream_key: str = Field(alias="REDIS_STREAM_KEY")

    #FUNNEL_BOT
    funnel_bot_webhook_url: str = Field(alias="FUNNEL_BOT_WEBHOOK_URL")
    funnel_bot_token: str = Field(alias="FUNNEL_BOT_TOKEN")
    funnel_bot_webhook_secret_token: str = Field(alias="FUNNEL_BOT_WEBHOOK_SECRET_TOKEN")

    #COURSE_BOT
    course_bot_link: str = "ССЫЛКА НА БОТА"

    #YOOKASSA
    shop_secret_key: str = Field(alias="SHOP_SECRET_KEY")
    shop_id: str = Field(alias="SHOP_ID")

    #APP Environment
    tz: str = Field(alias="TZ")
    app_env: Environment = Field(default=Environment.DEVELOPMENT, alias="APP_ENV")
    admin_ids: list[int] = Field(default_factory=list, alias="ADMIN_IDS")



    @property
    def is_dev(self) -> bool:
        return self.app_env == Environment.DEVELOPMENT

    @property
    def timezone(self):
        return pytz.timezone(self.tz)

settings = Settings()


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

