from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from backend.api.router import api_router
from contextlib import asynccontextmanager

from backend.database.session import Database
from backend.services.secret import Settings, AuthService


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()

    db = Database(settings)
    auth = AuthService(settings)

    db.create_tables()

    app.state.db = db
    app.state.auth_service = auth
    yield
    db.engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Marktplaats Watcher",
        lifespan=lifespan,
    )
    app.include_router(api_router)
    return app


app = create_app()
