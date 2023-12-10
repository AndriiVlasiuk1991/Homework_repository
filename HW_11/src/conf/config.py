class Config:
    SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:1111@localhost:5432/postgres"


config = Config
