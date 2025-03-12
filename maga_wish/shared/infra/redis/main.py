from redis.asyncio.client import Redis
import redis.asyncio as redis
import json
from typing import Any

from maga_wish.shared.environment.main import settings

def redisConnection():
    return redis.from_url(settings.REDIS_DATABASE_URI_STR)

class RedisDefault:
    def __init__(self):
        self.redisClient = redisConnection()

    @classmethod
    def connection(cls):
        return cls()

    async def shutdown(self):
        await self.redisClient.close()

    async def set(self, key: str, obj: Any):
        jsonDump = json.dumps(obj)
        await self.redisClient.set(key, jsonDump)

    async def get(self, key: str) -> Any:
        jsonObj = await self.redisClient.get(key)
        if jsonObj:
            return json.loads(jsonObj)

        return None