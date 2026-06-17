from datetime import datetime

from pydantic import BaseModel


class HealthRead(BaseModel):
    status: str