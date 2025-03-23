from fastapi import FastAPI
from starlette.middleware import Middleware

from api.routers import routers
from core.config import config
from core.fastapi.middlewares import SQLAlchemyMiddleware


def make_middleware():
    middleware = [
        Middleware(SQLAlchemyMiddleware)
    ]

    return middleware

def create_app() -> FastAPI:
    app_ = FastAPI(
        title=config.app.title,
        description=config.app.description,
        version=config.app.version,
        docs_url="/docs",
        middleware=make_middleware()
    )

    for router in routers:
        app_.include_router(router)

    return app_

app = create_app()
