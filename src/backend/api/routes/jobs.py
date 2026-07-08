# src/backend/api/routes/job_service.py

from fastapi import APIRouter, Depends, Request
from marktplaats import Condition

from backend.api.schemas.jobs import (
    SearchJobUpdate,
    SearchJobCreate,
    SearchJobResponse,
    SearchJobResponses,
)

from backend.services.job_service import JobService
from backend.services.secret import AuthService, Payload

router = APIRouter()


def get_service(request: Request) -> JobService:
    return JobService(db=request.app.state.db)


@router.post("/jobs/", response_model=SearchJobResponse)
async def create_job(job: SearchJobCreate, service: JobService = Depends(get_service)):

    return service.create_job(job)


@router.get("/jobs", response_model=SearchJobResponses)
async def get_jobs():
    "Returns a list of all jobs"
    jobs = None
    return jobs


@router.patch("/jobs/{job_id}")
async def update_job(job_id: str, job: SearchJobUpdate):
    updates = job.model_dump(exclude_unset=True)
    return {"id": job_id, "updates": updates}
