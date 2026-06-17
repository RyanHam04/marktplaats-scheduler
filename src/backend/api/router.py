from fastapi import APIRouter

from backend.api.routes import jobs, health

api_router = APIRouter()
api_router.include_router(jobs.router)
api_router.include_router(health.router)