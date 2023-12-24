from pydantic import ConfigDict, field_validator, EmailStr
from pydantic_settings import BaseSettings

from typing import Any


class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://postgres:567234@localhost:5432/postgres"
    SECRET_KEY_JWT: str = "63c03f8efb1573cd8154c8e4aad0f136e89a44d8fa473f642ab0fda99806daa8"
    ALGORITHM: str = "HS256"
    MAIL_USERNAME: str = "fatsapiuser@meta.ua"
    MAIL_PASSWORD: str = "pythonCourse2023"
    MAIL_FROM: str = "fatsapiuser@meta.ua"
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "smtp.meta.ua"
    REDIS_URL: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    CLD_NAME: str = "AV"
    CLD_API_KEY: int = "132698283185694"
    CLD_API_SECRET: str

    @field_validator("ALGORITHM")
    @classmethod
    def validate_algorithm(cls, v: Any):
        if v not in ["HS256", "HS512"]:
            raise ValueError("algorithm must be HS256 or HS512")
        return v

    model_config = ConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8")  # noqa


config = Settings()
