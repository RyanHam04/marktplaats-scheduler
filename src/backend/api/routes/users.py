# src/backend/api/routes/job_service.py

from fastapi import APIRouter, Depends, Request
from backend.api.schemas.users import UserCreate, UserResponse
from backend.services.job_service import JobService

router = APIRouter()


def get_service(request: Request) -> JobService:
    return JobService(db=request.app.state.db)



@router.post("/users", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    service: JobService = Depends(get_service),
):
    db_user = service.create_user(user)

    return UserResponse(
        id=db_user.id,
        notifier_params=db_user.notifier_params,
        token=db_user.token,
    )
