# src/backend/api/routes/common.py

from pydantic import BaseModel


class HealthRead(BaseModel):
    status: str
