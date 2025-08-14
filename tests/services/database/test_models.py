"""Tests to assert that the db model relationships work as expected"""

from datetime import date
from typing import Any, Callable

import pytest
from sqlalchemy.orm import Session

from open_cec_api.services.database.models import (
    Certificate,
    DeviceClass,
    DeviceClassAttribute,
    EntityType,
    Listing,
    ListingDeviceClass,
    ListingDeviceClassAttribute,
)


@pytest.mark.anyio
def test_entity_type_creation(
    db_session_fixture: Session,
    dummy_entity_type_factory: Callable[[Any], EntityType],
) -> None:
    """Assert that we can create and add an EntityType to the database"""

    d_et = dummy_entity_type_factory(name="foo")  # type: ignore
    retr = db_session_fixture.query(EntityType).filter_by(id=d_et.id).first()

    assert retr is not None
    assert retr.name == "foo"  # type: ignore
    assert retr.description == "dummy client"  # type: ignore

    assert retr.listings == []


def test_device_class_creation(
    db_session_fixture: Session,
    dummy_device_class_factory: Callable[[Any], DeviceClass],
):
    """Assert that we can create and add a DeviceClass to the database"""

    d_dc = dummy_device_class_factory(description="dummy inverter")  # type: ignore
    retr = db_session_fixture.query(DeviceClass).filter_by(id=d_dc.id).first()

    assert retr is not None
    assert retr.name == "bess"  # type: ignore
    assert retr.description == "dummy inverter"  # type: ignore


def test_listing_creation(
    db_session_fixture: Session,
    dummy_entity_type_factory: Callable[[Any], EntityType],
    dummy_listing_factory: Callable[[Any], Listing],
) -> None:
    """Assert that we can create and add a Listing to the database.

    Of this, we need to check that there are no certificates registered
    to a listing.
    """

    d_et = dummy_entity_type_factory()  # type: ignore
    d_l = dummy_listing_factory(entity_type_id=d_et.id)  # type: ignore

    retr = db_session_fixture.query(Listing).filter_by(id=d_l.id).first()
    assert len(retr.certificates) == 0  # type: ignore
    assert retr.status == "active"  # type: ignore
    # etc


def test_listing_device_class_creation(
    db_session_fixture: Session,
    dummy_device_class_factory: Callable[[Any], DeviceClass],
    dummy_entity_type_factory: Callable[[Any], EntityType],
    dummy_listing_factory: Callable[[Any], Listing],
    dummy_listing_device_class_factory: Callable[[Any], ListingDeviceClass],
) -> None:
    """Assert that we can create and add a ListingDeviceClass to the database"""

    d_dc = dummy_device_class_factory()  # type: ignore
    d_et = dummy_entity_type_factory()  # type: ignore
    d_l = dummy_listing_factory(entity_type_id=d_et.id)  # type: ignore

    d_ldc = dummy_listing_device_class_factory(
        listing_id=d_l.id,  # type: ignore
        device_class_id=d_dc.id,  # type: ignore
    )

    # this could be expanded
    retr = db_session_fixture.query(ListingDeviceClass).filter_by(id=d_ldc.id).first()
    assert retr is not None


def test_device_class_attribute_creation(
    db_session_fixture: Session,
    dummy_device_class_factory: Callable[[Any], DeviceClass],
    dummy_device_class_attribute_factory: Callable[[Any], DeviceClassAttribute],
) -> None:
    """Assert that we can create and add a DeviceClassAttribute to the database"""

    d_dc = dummy_device_class_factory()  # type: ignore
    d_dca = dummy_device_class_attribute_factory(device_class_id=d_dc.id)  # type: ignore

    retr = db_session_fixture.query(DeviceClassAttribute).filter_by(id=d_dca.id).first()
    assert retr.attribute_name == "foo"  # type: ignore
    assert retr.attribute_type == "number"  # type: ignore


def test_listing_device_class_attribute_creation(
    db_session_fixture: Session,
    dummy_entity_type_factory: Callable[[Any], EntityType],
    dummy_device_class_factory: Callable[[Any], DeviceClass],
    dummy_listing_factory: Callable[[Any], Listing],
    dummy_listing_device_class_attribute_factory: Callable[
        [Any], ListingDeviceClassAttribute
    ],
) -> None:
    """Assert that we can create and add a ListingDeviceClassAttribute to the database"""

    d_et = dummy_entity_type_factory()  # type: ignore
    d_dc = dummy_device_class_factory()  # type: ignore
    d_l = dummy_listing_factory(entity_type_id=d_et.id)  # type: ignore
    d_ldca = dummy_listing_device_class_attribute_factory(
        listing_id=d_l.id,  # type: ignore
        device_class_id=d_dc.id,  # type: ignore
    )

    retr = (
        db_session_fixture.query(ListingDeviceClassAttribute)
        .filter_by(id=d_ldca.id)
        .first()
    )
    assert retr.attribute_name == "foo"  # type: ignore
    assert retr.attribute_value == "bar"  # type: ignore


def test_certificate_creation(
    db_session_fixture: Session,
    dummy_entity_type_factory: Callable[[Any], EntityType],
    dummy_listing_factory: Callable[[Any], Listing],
    dummy_certificate_factory: Callable[[Any], Certificate],
) -> None:
    """Assert that we can create and add a Certificate to the database"""

    d_et = dummy_entity_type_factory()  # type: ignore
    d_l = dummy_listing_factory(entity_type_id=d_et.id)  # type: ignore
    d_c = dummy_certificate_factory(listing_id=d_l.id, test_profiles=["a", "b"])  # type: ignore

    retr = db_session_fixture.query(Certificate).filter_by(id=d_c.id).first()
    assert retr.certification_date == date(2000, 1, 1)  # type: ignore
    assert retr.certifying_body == "dummy certifier"  # type: ignore
    assert set(retr.test_profiles) == set(["a", "b"])  # type: ignore


def test_entity_type_listings_relationship(
    db_session_fixture: Session,
    dummy_entity_type_factory: Callable[[Any], EntityType],
    dummy_listing_factory: Callable[[Any], Listing],
) -> None:
    """Assert that when we create a listing, the entity type relationship
    is automatically updated (refresh is required though)"""

    d_et = dummy_entity_type_factory()  # type: ignore
    retr = db_session_fixture.query(EntityType).filter_by(id=d_et.id).first()
    assert retr.listings == []  # type: ignore

    d_l = dummy_listing_factory(entity_type_id=d_et.id)  # type: ignore
    db_session_fixture.refresh(d_et)
    retr2 = db_session_fixture.query(EntityType).filter_by(id=d_et.id).first()
    assert retr2.listings != []  # type: ignore

    retr3 = db_session_fixture.query(Listing).filter_by(id=d_l.id).first()
    assert retr3.entity_type.id == d_et.id  # type: ignore


def test_device_class_listing_device_class_relationship(
    db_session_fixture: Session,
    dummy_entity_type_factory: Callable[[Any], EntityType],
    dummy_device_class_factory: Callable[[Any], DeviceClass],
    dummy_listing_factory: Callable[[Any], Listing],
    dummy_listing_device_class_factory: Callable[[Any], ListingDeviceClass],
) -> None:
    """Assert that when we create a ListingDeviceClass, the DeviceClass
    relationship is automatically updated (after refresh)"""

    d_dc = dummy_device_class_factory()  # type: ignore
    d_et = dummy_entity_type_factory()  # type: ignore
    d_l = dummy_listing_factory(entity_type_id=d_et.id)  # type: ignore

    retr = db_session_fixture.query(DeviceClass).filter_by(id=d_dc.id).first()
    assert retr.listing_device_classes == []  # type: ignore

    dummy_listing_device_class_factory(
        listing_id=d_l.id,  # type: ignore
        device_class_id=d_dc.id,  # type: ignore
    )

    db_session_fixture.refresh(d_dc)
    retr2 = db_session_fixture.query(DeviceClass).filter_by(id=d_dc.id).first()
    assert retr2.listing_device_classes != []  # type: ignore


def test_device_class_device_class_attributes_relationship(
    db_session_fixture: Session,
    dummy_device_class_factory: Callable[[Any], DeviceClass],
    dummy_device_class_attribute_factory: Callable[[Any], DeviceClassAttribute],
):
    """Assert that when we create a DeviceClassAttribute, the DeviceClass
    relationship is automatically updated (after refresh)"""
    d_dc = dummy_device_class_factory()  # type: ignore

    retr = db_session_fixture.query(DeviceClass).filter_by(id=d_dc.id).first()
    assert retr.device_class_attributes == []  # type: ignore

    dummy_device_class_attribute_factory(device_class_id=d_dc.id)  # type: ignore
    db_session_fixture.refresh(d_dc)
    retr2 = db_session_fixture.query(DeviceClass).filter_by(id=d_dc.id).first()
    assert retr2.device_class_attributes != []  # type: ignore


def test_listing_listing_device_class_relationship(
    db_session_fixture: Session,
    dummy_device_class_factory: Callable[[Any], DeviceClass],
    dummy_entity_type_factory: Callable[[Any], EntityType],
    dummy_listing_factory: Callable[[Any], Listing],
    dummy_listing_device_class_factory: Callable[[Any], ListingDeviceClass],
):
    """Assert that when we create a ListingDeviceClass, the Listing
    relationship is automatically updated (after refresh)"""

    d_et = dummy_entity_type_factory()  # type: ignore
    d_dc = dummy_device_class_factory()  # type: ignore
    d_l = dummy_listing_factory(entity_type_id=d_et.id)  # type: ignore

    retr = db_session_fixture.query(Listing).filter_by(id=d_l.id).first()
    assert retr.listing_device_classes == []  # type: ignore

    d_ldc = dummy_listing_device_class_factory(
        listing_id=d_l.id,  # type: ignore
        device_class_id=d_dc.id,  # type: ignore
    )

    db_session_fixture.refresh(d_l)
    retr2 = db_session_fixture.query(Listing).filter_by(id=d_l.id).first()
    assert retr2.listing_device_classes != []  # type: ignore

    # assert that deleting the listing also deletes the listing_device_class
    # by virtue of cascade=all
    db_session_fixture.delete(d_l)
    db_session_fixture.flush()

    # assert the listing is gone
    retr3 = db_session_fixture.query(Listing).filter_by(id=d_l.id).first()
    assert retr3 is None

    # assert that the child listing device class is gone
    retr4 = db_session_fixture.query(ListingDeviceClass).filter_by(id=d_ldc.id).first()
    assert retr4 is None


def test_listing_listing_device_class_attribute_relationship(
    db_session_fixture: Session,
    dummy_device_class_factory: Callable[[Any], DeviceClass],
    dummy_entity_type_factory: Callable[[Any], EntityType],
    dummy_listing_factory: Callable[[Any], Listing],
    dummy_listing_device_class_attribute_factory: Callable[
        [Any], ListingDeviceClassAttribute
    ],
):
    """Assert that when we create a ListingDeviceClassAttribute, the Listing
    relationship is automatically updated (after refresh)"""

    d_et = dummy_entity_type_factory()  # type: ignore
    d_dc = dummy_device_class_factory()  # type: ignore
    d_l = dummy_listing_factory(entity_type_id=d_et.id)  # type: ignore

    retr = db_session_fixture.query(Listing).filter_by(id=d_l.id).first()
    assert retr.listing_device_class_attributes == []  # type: ignore

    d_ldca = dummy_listing_device_class_attribute_factory(
        listing_id=d_l.id,  # type: ignore
        device_class_id=d_dc.id,  # type: ignore
    )

    db_session_fixture.refresh(d_l)
    retr2 = db_session_fixture.query(Listing).filter_by(id=d_l.id).first()
    assert retr2.listing_device_class_attributes != []  # type: ignore

    # assert that deleting the listing also deletes the listing_device_class_attribute
    # by virtue of cascade=all
    db_session_fixture.delete(d_l)
    db_session_fixture.flush()

    # assert the listing is gone
    retr3 = db_session_fixture.query(Listing).filter_by(id=d_l.id).first()
    assert retr3 is None

    # assert that the child listing device class attribute is gone
    retr4 = (
        db_session_fixture.query(ListingDeviceClassAttribute)
        .filter_by(id=d_ldca.id)
        .first()
    )
    assert retr4 is None


def test_listing_certificate_relationship(
    db_session_fixture: Session,
    dummy_entity_type_factory: Callable[[Any], EntityType],
    dummy_listing_factory: Callable[[Any], Listing],
    dummy_certificate_factory: Callable[[Any], Certificate],
):
    """Assert that when we create a Certificate, the Listing
    relationship is automatically updated (after refresh)"""

    d_et = dummy_entity_type_factory()  # type: ignore
    d_l = dummy_listing_factory(entity_type_id=d_et.id)  # type: ignore

    retr = db_session_fixture.query(Listing).filter_by(id=d_l.id).first()
    assert retr.certificates == []  # type: ignore

    d_c = dummy_certificate_factory(listing_id=d_l.id, test_profiles=["a", "b"])  # type: ignore

    db_session_fixture.refresh(d_l)
    retr2 = db_session_fixture.query(Listing).filter_by(id=d_l.id).first()
    assert retr2.certificates != []  # type: ignore

    # assert that deleting the listing also deletes the listing_device_class_attribute
    # by virtue of cascade=all
    db_session_fixture.delete(d_l)
    db_session_fixture.flush()

    # assert the listing is gone
    retr3 = db_session_fixture.query(Listing).filter_by(id=d_l.id).first()
    assert retr3 is None

    # assert that the child certificate is gone
    retr4 = db_session_fixture.query(Certificate).filter_by(id=d_c.id).first()
    assert retr4 is None


def test_listing_unique_constraint(
    db_session_fixture: Session,
    dummy_entity_type_factory: Callable[[Any], EntityType],
    dummy_listing_factory: Callable[[Any], Listing],
):
    """Assert that we cannot create two listing with the same (manufacturer, model) combination"""

    d_et = dummy_entity_type_factory()  # type: ignore
    d_l1 = dummy_listing_factory(
        manufacturer="foo",  # type: ignore
        model="bar",
        entity_type_id=d_et.id,
    )

    retr = db_session_fixture.query(Listing).filter_by(id=d_l1.id).first()
    assert retr is not None

    # assert we can add a listing which does not violate the unique constraint
    dummy_listing_factory(
        manufacturer="foo2",  # type: ignore
        model="bar",
        entity_type_id=d_et.id,
    )

    retr2 = db_session_fixture.query(Listing).all()
    assert len(retr2) == 2

    # assert we cannot add a listing which does violate the unique constraint
    with pytest.raises(Exception):
        dummy_listing_factory(
            manufacturer="foo2",  # type: ignore
            model="bar",
            entity_type_id=d_et.id,
        )

    # we cannot query the outcome here because we will be in a dirty state, but we cannot rollback
    # because we don't commit the first two instances.


def test_listing_device_class_unique_constraint(
    db_session_fixture: Session,
    dummy_device_class_factory: Callable[[Any], DeviceClass],
    dummy_entity_type_factory: Callable[[Any], EntityType],
    dummy_listing_factory: Callable[[Any], Listing],
    dummy_listing_device_class_factory: Callable[[Any], ListingDeviceClass],
):
    """Assert that we cannot create two ListingDeviceClasses with the same (listing_id, device_class_id) combination"""

    d_dc = dummy_device_class_factory()  # type: ignore
    d_et = dummy_entity_type_factory()  # type: ignore
    d_l1 = dummy_listing_factory(model="model1", entity_type_id=d_et.id)  # type: ignore
    d_l2 = dummy_listing_factory(model="model2", entity_type_id=d_et.id)  # type: ignore

    dummy_listing_device_class_factory(
        listing_id=d_l1.id,  # type: ignore
        device_class_id=d_dc.id,  # type: ignore
    )

    retr = db_session_fixture.query(ListingDeviceClass).all()
    assert len(retr) == 1  # type: ignore

    # assert we can add a ldc that does not violate the unique constraint
    dummy_listing_device_class_factory(
        listing_id=d_l2.id,  # type: ignore
        device_class_id=d_dc.id,  # type: ignore
    )

    retr2 = db_session_fixture.query(ListingDeviceClass).all()
    assert len(retr2) == 2  # type: ignore

    # assert we cannot add a ldc that does violate the unique constraint
    with pytest.raises(Exception):
        dummy_listing_device_class_factory(
            listing_id=d_l1.id,  # type: ignore
            device_class_id=d_dc.id,  # type: ignore
        )

    # we cannot query the outcome here because we will be in a dirty state, but we cannot rollback
    # because we don't commit the first two instances.


def test_device_class_attribute_unique_constraint():
    # TODO
    pass


def test_listing_device_class_attribute_unique_constraint():
    # TODO
    pass
