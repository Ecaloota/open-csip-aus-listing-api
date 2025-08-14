from datetime import date
from typing import Generator

import pytest
import sqlalchemy
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer

from open_cec_api.api.schema.enums import StatusEnum
from open_cec_api.services.database.models import (
    Base,
    Certificate,
    DeviceClass,
    DeviceClassAttribute,
    EntityType,
    Listing,
    ListingDeviceClass,
    ListingDeviceClassAttribute,
)


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="module")
def db_engine_fixture():
    with PostgresContainer("postgres:16") as postgres:
        engine = sqlalchemy.create_engine(postgres.get_connection_url())
        Base.metadata.create_all(bind=engine)
        yield engine
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session_fixture(
    db_engine_fixture: sqlalchemy.Engine,
) -> Generator[Session, None, None]:
    connection = db_engine_fixture.connect()
    transaction = connection.begin()

    session_maker = sessionmaker(
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        bind=connection,
    )
    session = session_maker()
    try:
        yield session
    finally:
        session.close()
        if transaction.is_active:
            transaction.rollback()
        connection.close()


@pytest.fixture
def dummy_entity_type_factory(db_session_fixture: Session):
    def _create(**kwargs):
        defaults = {"name": "client", "description": "dummy client"}
        defaults.update(kwargs)
        model = EntityType(**defaults)
        db_session_fixture.add(model)
        db_session_fixture.commit()
        return model

    return _create


@pytest.fixture
def dummy_device_class_factory(db_session_fixture: Session):
    def _create(**kwargs):
        defaults = {"name": "bess", "description": "dummy bess"}
        defaults.update(kwargs)
        model = DeviceClass(**defaults)
        db_session_fixture.add(model)
        db_session_fixture.commit()
        return model

    return _create


@pytest.fixture
def dummy_listing_factory(db_session_fixture: Session):
    def _create(**kwargs):
        defaults = {
            "manufacturer": "dummy manufacturer",
            "model": "dummy model",
            "status": StatusEnum.active,
        }
        defaults.update(kwargs)
        model = Listing(**defaults)
        db_session_fixture.add(model)
        db_session_fixture.commit()
        return model

    return _create


@pytest.fixture
def dummy_listing_device_class_factory(db_session_fixture: Session):
    def _create(**kwargs):
        defaults = {}
        defaults.update(kwargs)
        model = ListingDeviceClass(**defaults)
        db_session_fixture.add(model)
        db_session_fixture.commit()
        return model

    return _create


@pytest.fixture
def dummy_device_class_attribute_factory(db_session_fixture: Session):
    def _create(**kwargs):
        defaults = {
            "attribute_name": "foo",
            "attribute_type": "number",
            "description": "dummy attribute",
        }
        defaults.update(kwargs)
        model = DeviceClassAttribute(**defaults)
        db_session_fixture.add(model)
        db_session_fixture.commit()
        return model

    return _create


@pytest.fixture
def dummy_listing_device_class_attribute_factory(db_session_fixture: Session):
    def _create(**kwargs):
        defaults = {
            "attribute_name": "foo",
            "attribute_value": "bar",
        }
        defaults.update(kwargs)
        model = ListingDeviceClassAttribute(**defaults)
        db_session_fixture.add(model)
        db_session_fixture.commit()
        return model

    return _create


@pytest.fixture
def dummy_certificate_factory(db_session_fixture: Session):
    def _create(**kwargs):
        defaults = {
            "expiry": date(year=2000, month=1, day=1),
            "certification_date": date(year=2000, month=1, day=1),
            "certifying_body": "dummy certifier",
        }
        defaults.update(kwargs)
        model = Certificate(**defaults)
        db_session_fixture.add(model)
        db_session_fixture.commit()
        return model

    return _create
