# src/backend/api/schemas/job_service.py

from datetime import datetime
from enum import Enum
from typing import Any

from marktplaats import SortBy, SortOrder, Condition, category_from_name
from pydantic import BaseModel, Field, model_validator
from typing_extensions import Annotated

from backend.api.schemas.notifiers import (
    NtfyNotifierParams,
    TelegramNotifierParams,
    EmailNotifierParams,
)


class ConditionRequest(str, Enum):
    NEW = "NEW"
    REFURBISHED = "REFURBISHED"
    AS_GOOD_AS_NEW = "AS_GOOD_AS_NEW"
    USED = "USED"
    NOT_WORKING = "NOT_WORKING"


class SearchJobBase(BaseModel):
    email: str
    token: str
    query: str = ""
    zip_code: str | None = None
    distance: int | None = None
    price_from: int | None = None
    price_to: int | None = None
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    sort_by: SortBy = SortBy.OPTIMIZED
    sort_order: SortOrder = SortOrder.ASC
    condition: ConditionRequest | None = None
    offered_since: datetime | None = None
    category_name: str | None = None
    extra_attributes: list[int] | None = None
    check_interval: int = Field(default=3600, ge=0)  # seconds

    @model_validator(mode="after")
    def validate(self):
        if not self.query and not self.category_name:
            msg = (
                "Invalid arguments: When the query is empty, "
                "a category must be specified."
            )
            raise ValueError(msg)

        if self.category_name:
            try:
                print(category_from_name(self.category_name))
            except ValueError:  # Should become dropdown menu in frontend
                msg = (
                    "Invalid arguments: Category not available, "
                    "please check the available categories"
                )
                raise ValueError(msg)
        return self


class SearchJobCreate(SearchJobBase):
    """Request body for creating a job."""

    model_validator(mode="after")

    def format_condition(self):
        if self.condition is not None:
            self.condition = Condition[self.condition.name]
        return self


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
