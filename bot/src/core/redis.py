from redis.asyncio import Redis
from src.core.config import settings


def init_redis():
    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True
    )