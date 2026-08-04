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


class SearchParams(BaseModel):
    query: str = ""
    zip_code: str | None = None
    distance_km: int | None = None
    price_from: int | None = None
    price_to: int | None = None
    condition: str | None = None
    category_name: str | None = None
    extra_attributes: list[int] | None = None

    @model_validator(mode="after")
    def validate(self):
        if not self.query and not self.category_name:
            msg = (
                "Invalid arguments: When the query is empty, "
                "a category must be specified."
            )
            raise ValueError(msg)

        if self.distance_km is None or self.zip_code is None:
            raise ValueError(
                "zip_code and distance are required."
            )

        if self.category_name:
            try:
                category_from_name(self.category_name)
            except ValueError:  # Should become dropdown menu in frontend
                msg = (
                    "Invalid arguments: Category not available, "
                    "please check the available categories"
                )
                raise ValueError(msg)
        if (
            self.price_from is not None
            and self.price_to is not None
            and self.price_from > self.price_to
        ):
            msg = (
                "price_from cannot be greater than price_to."
            )
            raise ValueError(msg)

        return self


class SearchJobCreate(BaseModel):
    token: str
    search: SearchParams
    check_interval: int = Field(default=3600)

class SearchParamsUpdate(BaseModel):
    query: str | None = None
    zip_code: str | None = None
    distance_km: int | None = None
    price_from: int | None = None
    price_to: int | None = None
    condition: ConditionRequest | None = None
    category_name: str | None = None
    extra_attributes: list[int] | None = None


class SearchJobUpdate(BaseModel):
    search: SearchParamsUpdate | None = None
    check_interval: int | None = Field(default=None)
    enabled: bool | None = None

class SearchJobResponse(BaseModel):
    id: int


class SearchJobResponses(BaseModel):
    jobs: list[SearchJobResponse]
