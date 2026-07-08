import json
import jwt
from pydantic import model_validator, BaseModel

from pydantic_settings import BaseSettings


class Payload(BaseModel):
    user_id: str


class Settings(BaseSettings):
    db_host: str
    db_user: str
    db_password: str
    db_name: str

    secret: str
    algorithm: str

    class Config:
        env_file = ".env"


class AuthService:
    def __init__(self, settings: Settings):
        self.secret = settings.secret
        self.algorithm = settings.algorithm

    def create(self, payload: Payload):
        return jwt.encode(
            payload.model_dump(), key=self.secret, algorithm=self.algorithm
        )
