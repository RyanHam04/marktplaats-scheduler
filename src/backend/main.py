from fastapi import FastAPI

from backend.api.router import api_router
from contextlib import asynccontextmanager

from backend.database.session import Database


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = Database()
    db.drop_tables()
    db.create_tables()
    app.state.db = db

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