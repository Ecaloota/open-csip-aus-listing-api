"""Perform database initialization tasks, if requested."""

from loguru import logger

from open_cec_api.api.v1.models import SoftwareCommsClientModel_V1
from open_cec_api.services.database.db import ensure_session


# TODO this is a temporary way to initialize the database
async def init_db():
    logger.info("Initializing database...")
    async with ensure_session() as session:
        model = SoftwareCommsClientModel_V1(
            Communication_Device_Name__c=None,
            Communication_Manufacturer__c=None,
            Communication_Manufacturer_Name__c=None,
            Communication_Model_Name__c=None,
        )

        session.add(model)
        session.commit()

    return
