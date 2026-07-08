# src/backend/api/schemas/job_service.py

from datetime import datetime
from enum import Enum
from typing import Any, Literal

from marktplaats import SortBy, SortOrder, Condition, category_from_name
from pydantic import BaseModel, Field, model_validator


class NotifierParams(BaseModel):
    pass


class NtfyNotifierParams(NotifierParams):
    type: Literal["ntfy"]
    topic: str
    username: str | None = None
    password: str | None = None
    token: str | None = None

    @model_validator(mode="after")
    def validate_auth(self):
        if bool(self.username) ^ bool(self.password):
            msg = (
                "Invalid arguments for the notifier: "
                "Either both username AND password have to be set, or neither"
            )
            raise ValueError(msg)

        elif self.token and self.username:
            msg = (
                "Invalid arguments for the notifier: "
                "Enter either a token OR credentials"
            )
            raise ValueError(msg)
        return self


class TelegramNotifierParams(NotifierParams):
    type: Literal["telegram"]

    @model_validator(mode="after")
    def validate_auth(self):
        raise NotImplementedError


class EmailNotifierParams(NotifierParams):
    type: Literal["email"]

    @model_validator(mode="after")
    def validate_auth(self):
        raise NotImplementedError
