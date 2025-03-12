from redis.asyncio.client import Redis
import redis.asyncio as redis

from maga_wish.shared.environment.main import settings

def redisConnection() -> Redis:
    return redis.from_url(settings.REDIS_DATABASE_URI_STR)

async def shutdown(redisClient: Redis):
    await redisClient.close()