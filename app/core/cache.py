import redis.asyncio as aioredis
from app.core.config import settings


def get_redis_client():
    return aioredis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
    )


async def get_cached(key: str) -> str | None:
    if settings.testing:
        return None
    try:
        client = get_redis_client()
        return await client.get(key)
    except Exception:
        return None


async def set_cached(key: str, value: str, expire_seconds: int = 60) -> None:
    if settings.testing:
        return
    try:
        client = get_redis_client()
        await client.set(key, value, ex=expire_seconds)
    except Exception:
        pass


async def delete_cached(key: str) -> None:
    if settings.testing:
        return
    try:
        client = get_redis_client()
        await client.delete(key)
    except Exception:
        pass
