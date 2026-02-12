import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from open_cec_api.api.admin_router import admin_router
from open_cec_api.api.public_router import public_router
from open_cec_api.services.database.db import engine, ensure_session
from open_cec_api.services.database.initialisation import init_db
from open_cec_api.services.database.models import Base


def reset_db():
    """
    Reset the database by dropping and creating tables based on the schema version.
    This is primarily used for development purposes.
    """

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with ensure_session() as session:
        init_db(session)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for the Open CEC API.
    This is used to manage startup and shutdown events.
    """
    # Perform any startup tasks here
    run_env = os.environ.get("run_env", "dev")
    if run_env not in ["dev", "prod"]:
        logger.error(f"Invalid run environment: {run_env}")
        raise ValueError(f"Invalid run environment: {run_env}")

    # Create the database tables if dev environment
    # this will be handled by alembic migrations in prod
    # and perform db initialization
    if run_env == "dev":
        logger.info("Creating database tables")
        reset_db()  # type: ignore[arg-type]

    app.include_router(public_router)
    app.include_router(admin_router)

    yield

    # Perform any shutdown tasks here


app = FastAPI(title="Open CSIP-AUS Listing API", lifespan=lifespan)
