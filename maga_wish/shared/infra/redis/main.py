from redis.asyncio.client import Redis
import redis.asyncio as redis
import json
from typing import Any

from maga_wish.shared.environment.main import settings

def redisConnection() -> Redis:
    return redis.from_url(settings.REDIS_DATABASE_URI_STR)

async def shutdown(redisClient: Redis):
    await redisClient.close()

class RedisDefault:
    async def set(key: str, obj: Any, redisClient: Redis):
        jsonDump = json.dumps(obj)
        await redisClient.set(key, jsonDump)

    async def get(key: str, redisClient: Redis) -> Any:
        jsonObj = await redisClient.get(key)
        if jsonObj:
            return json.loads(jsonObj)

        return None