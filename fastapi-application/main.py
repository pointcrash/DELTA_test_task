import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.sessions import SessionMiddleware

from core.config import settings

from api import router as api_router
from core.models import db_helper
from tasks import scheduler
from utils import redis

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    scheduler.start()
    yield
    # shutdown
    scheduler.shutdown()
    await db_helper.dispose()
    await redis.close()


main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

main_app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session.secret,
)

main_app.include_router(
    api_router,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
