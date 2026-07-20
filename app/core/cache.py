import redis.asyncio as aioredis
from app.core.config import settings

redis_client = aioredis.from_url(
    settings.redis_url,
    encoding="utf-8",
    decode_responses=True,
)


async def get_cached(key: str) -> str | None:
    return await redis_client.get(key)


async def set_cached(key: str, value: str, expire_seconds: int = 60) -> None:
    await redis_client.set(key, value, ex=expire_seconds)


async def delete_cached(key: str) -> None:
    await redis_client.delete(key)
