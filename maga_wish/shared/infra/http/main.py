from fastapi import FastAPI
from fastapi.routing import APIRoute
from contextlib import asynccontextmanager

from maga_wish.shared.infra.routes.main import api_router 
from maga_wish.shared.environment.main import settings
from maga_wish.shared.infra.redis.main import (
    redisConnection,
    shutdown
)

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Redis connection")
    redisClient = redisConnection()
    app.state.redis = redisClient

    yield

    print("Closing Redis connection")
    await shutdown(redisClient)

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    # openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

app.include_router(api_router, prefix=settings.API_V1_STR)