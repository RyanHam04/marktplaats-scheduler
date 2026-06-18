# src/backend/api/routes/job_service.py

from fastapi import APIRouter, Depends, Request
from backend.api.schemas.jobs import SearchJobCreate, SearchJobResponse
from backend.api.schemas.users import UserRequest, UserResponse
from backend.services.job_service import JobService
router = APIRouter()


def get_service(request: Request) -> JobService:
    return JobService(db=request.app.state.db)

@router.post("/users", response_model=UserResponse)
async def create_user(
    user: UserRequest,
    service: JobService = Depends(get_service)):
    return service.create_user(user)





