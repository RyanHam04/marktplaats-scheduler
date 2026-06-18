# src/backend/api/schemas/job_service.py

from datetime import datetime
from marktplaats import SortBy, SortOrder, Condition
from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    email: str


class UserResponse(BaseModel):
    email: str
    id: int