# src/backend/api/routes/job_service.py

from fastapi import APIRouter, Depends, Request


from backend.api.schemas.jobs import SearchJobCreate, SearchJobResponse
from backend.api.schemas.users import UserBase, UserDelete, UserCreate, UserResponse
from backend.database.models import User
from backend.services.job_service import JobService
from backend.notifications.service import create_notifier
from backend.services.secret import AuthService, Payload

router = APIRouter()


def get_service(request: Request) -> JobService:
    return JobService(db=request.app.state.db)


@router.post("/users", response_model=UserResponse)
async def create_user(
    user: UserCreate, request: Request, service: JobService = Depends(get_service)
):
    db_user = service.create_user(user)

    return UserResponse(
        id=db_user.id,
        email=db_user.email,
        notifier_params=db_user.notifier_params,
        token=db_user.token,
    )
