from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.sessions import SessionMiddleware

from core.config import settings

from api import router as api_router
from core.models import db_helper
from tasks import scheduler
from utils import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    scheduler.start()
    yield
    # shutdown
    scheduler.shutdown()
    await db_helper.dispose()
    await redis.close()


def create_app() -> FastAPI:
    app = FastAPI(
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.session.secret,
    )

    app.include_router(
        api_router,
    )

    return app
