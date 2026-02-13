from redis.asyncio import Redis
from src.core.config import settings


def init_redis():
    return Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        decode_responses=True
    )