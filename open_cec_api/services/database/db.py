from contextlib import contextmanager
from typing import Generator

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class DatabaseSettings(BaseSettings):
    dialect: str = "postgresql"
    user: str = "db_user"
    password: str = "db_pass"
    host: str = "postgres"  # Default to 'postgres' for Docker setup
    name: str = "cec_db"

    @property
    def database_url(self) -> str:
        return f"{self.dialect}://{self.user}:{self.password}@{self.host}/{self.name}"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="DB_", extra="allow")


db_settings = DatabaseSettings()  # type: ignore[call-arg] # instantiated at runtime


engine = create_engine(db_settings.database_url)
session_maker = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)


@contextmanager
def ensure_session() -> Generator[Session, None, None]:
    session = session_maker()
    try:
        yield session
    finally:
        session.close()


def get_db_session() -> Generator[Session, None, None]:
    """FastAPI dependency for database sessions."""
    session = session_maker()
    try:
        yield session
    finally:
        session.close()
