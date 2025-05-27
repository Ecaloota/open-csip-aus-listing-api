import os
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI
from loguru import logger

from open_cec_api.api.v1.models import BaseV1
from open_cec_api.api.v1.router import router as v1_router
from open_cec_api.api.v2.models import BaseV2
from open_cec_api.api.v2.router import router as v2_router
from open_cec_api.services.database.db import engine
from open_cec_api.services.database.setup import init_db
from open_cec_api.settings import settings


async def reset_db(schema_version: Literal["v1", "v2"]):
    """
    Reset the database by dropping and creating tables based on the schema version.
    This is primarily used for development purposes.
    """
    if schema_version == "v1":
        BaseV1.metadata.drop_all(bind=engine)
        BaseV1.metadata.create_all(bind=engine)
        await init_db()
    else:
        BaseV2.metadata.drop_all(bind=engine)
        BaseV2.metadata.create_all(bind=engine)


def add_router(app: FastAPI, schema_version: Literal["v1", "v2"]):
    """
    Add the appropriate router to the FastAPI application based on the
    schema version.
    """
    if schema_version == "v1":
        app.include_router(v1_router)
    else:
        app.include_router(v2_router)


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

    schema_version = settings.schema_version
    if schema_version not in ["v1", "v2"]:
        logger.error(f"Invalid schema version: {schema_version}")
        raise ValueError(f"Invalid schema version: {schema_version}")

    # Create the database tables if dev environment
    # this will be handled by alembic migrations in prod
    # and perform db initialization
    if run_env == "dev":
        logger.info("Creating database tables")
        await reset_db(schema_version)  # type: ignore[arg-type]

    # add the relevant router to the app
    add_router(app, schema_version)  # type: ignore[arg-type]

    yield

    # Perform any shutdown tasks here


app = FastAPI(title="Open CEC API", lifespan=lifespan)
