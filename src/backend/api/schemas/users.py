# src/backend/api/schemas/job_service.py

from datetime import datetime
from typing import Annotated

from marktplaats import SortBy, SortOrder, Condition
from pydantic import BaseModel, Field, model_validator

from backend.api.schemas.notifiers import (
    NtfyNotifierParams,
    TelegramNotifierParams,
    EmailNotifierParams,
)


class UserBase(BaseModel):
    pass

class UserCreate(UserBase):
    notifier_params: Annotated[
        NtfyNotifierParams | TelegramNotifierParams | EmailNotifierParams,
        Field(discriminator="type"),
    ]


class UserDelete(UserBase):
    id: int
    token: str


class UserResponse(BaseModel):
    id: int
    token: str
    notifier_params: NtfyNotifierParams | TelegramNotifierParams | EmailNotifierParams
