# src/backend/api/routes/health.py

from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from backend.api.schemas.common import HealthRead

router = APIRouter()

@router.get(f"/", response_model=HealthRead, status_code=HTTP_200_OK)
async def get_health():
    return HealthRead(status='ok')


