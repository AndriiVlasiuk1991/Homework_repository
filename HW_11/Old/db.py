from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.sqlite"
# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:1111@localhost:5432/rest_app"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
