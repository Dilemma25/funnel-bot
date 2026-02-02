from redis.asyncio import Redis
from src.core.config import config


def init_redis():
    return Redis(
        host=config['REDIS']['HOST'],
        port=config['REDIS']['PORT'],
        db=config['REDIS']['DB'],
        decode_responses=True
    )