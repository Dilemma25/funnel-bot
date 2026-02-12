# bot/src/storage/hybrid_storage.py
from aiogram.fsm.storage.base import BaseStorage, StateType, StorageKey
from aiogram.fsm.storage.redis import RedisStorage
from typing import Optional, Dict, Any

from src.models.user_state import UserState
from src.core.logging_config import setup_logging

logger = setup_logging(__name__, service="bot")


class HybridStorage(BaseStorage):
    """
    Гибридное хранилище FSM:
    - Основное: Redis (быстро)
    - Резервное: PostgreSQL (надежно)
    """

    def __init__(self, redis_storage: RedisStorage):
        self.redis = redis_storage

    async def set_state(
            self,
            key: StorageKey,
            state: StateType = None
    ) -> None:
        """Сохранить состояние в Redis + PostgreSQL"""

        # 1. Сохраняем в Redis (основное)
        await self.redis.set_state(key, state)

        # 2. Сохраняем в PostgreSQL (резервная копия)
        try:
            state_name = state.state if state else None

            await UserState.update_or_create(
                user_id=key.user_id,
                defaults={"state": state_name}
            )

            logger.debug(f"✅ State saved to DB: user={key.user_id}, state={state_name}")

        except Exception as e:
            logger.error(f"❌ Failed to save state to DB: {e}")
            # Не падаем, Redis уже сохранил

    async def get_state(
            self,
            key: StorageKey
    ) -> Optional[str]:
        """Получить состояние: сначала Redis, потом PostgreSQL"""

        # 1. Пытаемся взять из Redis
        try:
            state = await self.redis.get_state(key)

            if state:
                logger.debug(f"🔵 State from Redis: user={key.user_id}, state={state}")
                return state

        except Exception as e:
            logger.warning(f"⚠️ Redis failed, trying DB: {e}")

        # 2. Fallback на PostgreSQL
        try:
            user_state = await UserState.get_or_none(user_id=key.user_id)

            if user_state and user_state.state:
                logger.info(f"🟢 State from DB (fallback): user={key.user_id}, state={user_state.state}")

                # Восстанавливаем в Redis
                await self.redis.set_state(key, user_state.state)

                # если упал state то так же восстанавливаем дату
                await self.redis.set_data(key, user_state.data)

                return user_state.state

        except Exception as e:
            logger.error(f"❌ DB fallback failed: {e}")

        return None

    async def set_data(
            self,
            key: StorageKey,
            data: Dict[str, Any]
    ) -> None:
        """Сохранить FSM data в Redis + PostgreSQL"""

        # 1. Сохраняем в Redis
        await self.redis.set_data(key, data)

        # 2. Сохраняем в PostgreSQL
        try:
            await UserState.update_or_create(
                user_id=key.user_id,
                defaults={"data": data}
            )

            logger.debug(f"✅ Data saved to DB: user={key.user_id}")

        except Exception as e:
            logger.error(f"❌ Failed to save data to DB: {e}")

    async def update_data(
            self,
            key: StorageKey,
            data: Dict[str, Any]
    ) -> None:
        """Обновить FSM data в Redis + PostgreSQL (merge с существующими)"""

        # 1. Обновляем в Redis
        await self.redis.update_data(key, data)

        # 2. Обновляем в PostgreSQL
        try:
            user_state = await UserState.get_or_none(user_id=key.user_id)

            if user_state:
                # Мержим данные (как в Redis)
                existing_data = user_state.data or {}
                updated_data = {**existing_data, **data}

                user_state.data = updated_data
                await user_state.save()
            else:
                # Если записи нет - создаём
                await UserState.create(
                    user_id=key.user_id,
                    data=data
                )

            logger.debug(f"✅ Data updated in DB: user={key.user_id}")

        except Exception as e:
            logger.error(f"❌ Failed to update data in DB: {e}")
            # Не падаем, Redis уже обновил

    async def get_data(
            self,
            key: StorageKey
    ) -> Dict[str, Any]:
        """Получить FSM data: сначала Redis, потом PostgreSQL"""

        # 1. Пытаемся взять из Redis
        try:
            data = await self.redis.get_data(key)

            if data:
                logger.debug(f"🔵 Data from Redis: user={key.user_id}")
                return data

        except Exception as e:
            logger.warning(f"⚠️ Redis failed for data, trying DB: {e}")

        # 2. Fallback на PostgreSQL
        try:
            user_state = await UserState.get_or_none(user_id=key.user_id)

            if user_state:
                logger.info(f"🟢 Data from DB (fallback): user={key.user_id}")

                # Восстанавливаем в Redis
                await self.redis.set_data(key, user_state.data)

                return user_state.data

        except Exception as e:
            logger.error(f"❌ DB fallback failed for data: {e}")

        return {}

    async def close(self) -> None:
        """Закрыть соединения"""
        await self.redis.close()