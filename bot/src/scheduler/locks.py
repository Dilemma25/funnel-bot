import redis
from src.core.redis import init_redis
from src.core.config import config

class RedisLock:
    def __init__(self):
        self.lock_key = config['SCHEDULER_LOCK_KEY']
        self.redis = init_redis()
        self.lock = None

    def connect(self):
        self.lock = self.redis.lock(
            self.lock_key,
            blocking=True,
            blocking_timeout=5,
            timeout=70,
        )

    async def acquire(self) -> bool:
        return await self.lock.acquire()

    async def release(self) -> bool:
        try:
            await self.lock.release()
            return True
        except redis.exceptions.LockError:
            return False

    async def close(self):
        if self.redis:
            await self.redis.close()