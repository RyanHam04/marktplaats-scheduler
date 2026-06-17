from fastapi import APIRouter
from backend.api.schemas.common import HealthRead

router = APIRouter()

@router.get(f"/", response_model=HealthRead)
async def get_health(health: HealthRead):
    return health


