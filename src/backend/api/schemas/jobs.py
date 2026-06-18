# src/backend/api/schemas/job_service.py

from datetime import datetime
from marktplaats import SortBy, SortOrder, Condition
from pydantic import BaseModel, Field


class SearchJobBase(BaseModel):
    email: str
    query: str = ""
    zip_code: str | None = None
    distance: int | None = None
    price_from: int | None = None
    price_to: int | None = None
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    sort_by: SortBy = SortBy.OPTIMIZED
    sort_order: SortOrder = SortOrder.ASC
    condition: Condition | None = None
    offered_since: datetime | None = None
    category_name: str | None = None
    extra_attributes: list[int] | None = None
    check_interval: int = Field(default=3600, ge=60) # seconds


class SearchJobCreate(SearchJobBase):
    """Request body for creating a job."""
    pass


class SearchJobUpdate(BaseModel):
    """Request body for updating a job."""
    query: str | None = None
    zip_code: str | None = None
    distance: int | None = None
    price_from: int | None = None
    price_to: int | None = None
    limit: int | None = Field(default=None, ge=1, le=100)
    offset: int | None = Field(default=None, ge=0)
    sort_by: SortBy | None = None
    sort_order: SortOrder | None = None
    condition: Condition | None = None
    offered_since: datetime | None = None
    category_name: str | None = None
    extra_attributes: list[int] | None = None


class SearchJobResponse(BaseModel):
    """Response body."""
    id: int

class SearchJobResponses(BaseModel):
    jobs: list[SearchJobResponse]