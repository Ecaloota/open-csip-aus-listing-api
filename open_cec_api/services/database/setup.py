"""Perform database initialization tasks, if requested."""

from loguru import logger

from open_cec_api.services.database.db import ensure_session
from open_cec_api.services.database.models import EntityType


# TODO this is a temporary way to initialize the database
async def init_db():
    logger.info("Initializing database...")
    async with ensure_session() as session:
        model = EntityType(
            id=1,
            name="client",
            description="dummy client",
        )

        session.add(model)
        session.commit()

    return
