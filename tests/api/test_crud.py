from datetime import date
from typing import Protocol

import pytest
from sqlalchemy.orm import Session

from open_cec_api.api.crud import (
    CertificateCRUD,
    DeviceClassAttributeCRUD,
    DeviceClassCRUD,
    EntityTypeCRUD,
    KeyCRUD,
    ListingCRUD,
    ListingDeviceClassAttributeCRUD,
    ListingDeviceClassCRUD,
)
from open_cec_api.api.schema.create import (
    CertificateCreate,
    DeviceClassAttributeCreate,
    DeviceClassCreate,
    EntityTypeCreate,
    KeyCreate,
    ListingCreate,
    ListingDeviceClassAttributeCreate,
    ListingDeviceClassCreate,
)
from open_cec_api.api.schema.enums import AttributeTypeEnum, StatusEnum
from open_cec_api.api.schema.update import (
    CertificateUpdate,
    DeviceClassAttributeUpdate,
    DeviceClassUpdate,
    EntityTypeUpdate,
    KeyUpdate,
    ListingDeviceClassAttributeUpdate,
    ListingUpdate,
)
from open_cec_api.services.database.models import (
    Certificate,
    DeviceClass,
    DeviceClassAttribute,
    EntityType,
    Key,
    Listing,
    ListingDeviceClass,
    ListingDeviceClassAttribute,
)


class HasIdProtocol(Protocol):
    id: int


class TestKeyCRUD:
    def test_create(self, db_session_fixture: Session):
        """Test creating a new Key."""
        key_data = KeyCreate(value="hashed_key_123", description="Test API key")
        result = KeyCRUD.create(db_session_fixture, key_data)

        assert result.id is not None
        assert result.value == "hashed_key_123"
        assert result.description == "Test API key"

    def test_get_by_id(self, db_session_fixture: Session):
        """Test getting a Key by ID."""
        # Create a key first
        key_data = KeyCreate(value="hashed_key_123", description="Test API key")
        created_key = KeyCRUD.create(db_session_fixture, key_data)

        # Get by ID
        result = KeyCRUD.get(db_session_fixture, id=created_key.id)

        assert result is not None
        assert isinstance(result, Key)
        assert result.id == created_key.id
        assert result.value == "hashed_key_123"
        assert result.description == "Test API key"

    def test_get_by_id_not_found(self, db_session_fixture: Session):
        """Test getting a Key by non-existent ID."""
        result = KeyCRUD.get(db_session_fixture, id=999)
        assert result is None

    def test_get_all(self, db_session_fixture: Session):
        """Test getting all Keys."""
        # Create multiple keys
        key1_data = KeyCreate(value="key1", description="First key")
        key2_data = KeyCreate(value="key2", description="Second key")

        KeyCRUD.create(db_session_fixture, key1_data)
        KeyCRUD.create(db_session_fixture, key2_data)

        # Get all
        result = KeyCRUD.get(db_session_fixture)

        assert isinstance(result, list)
        assert len(result) == 2
        assert any(key.value == "key1" for key in result)
        assert any(key.value == "key2" for key in result)

    def test_get_with_filters(self, db_session_fixture: Session):
        """Test getting Keys with filters."""
        # Create multiple keys
        key1_data = KeyCreate(value="key1", description="Admin key")
        key2_data = KeyCreate(value="key2", description="User key")

        KeyCRUD.create(db_session_fixture, key1_data)
        KeyCRUD.create(db_session_fixture, key2_data)

        # Filter by description
        result = KeyCRUD.get(db_session_fixture, description="Admin")

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].description == "Admin key"

    def test_update(self, db_session_fixture: Session):
        """Test updating a Key."""
        # Create a key
        key_data = KeyCreate(value="original_key", description="Original description")
        created_key = KeyCRUD.create(db_session_fixture, key_data)

        # Update it
        update_data = KeyUpdate(description="Updated description")
        result = KeyCRUD.update(db_session_fixture, created_key.id, update_data)

        assert result is not None
        assert result.id == created_key.id
        assert result.value == "original_key"  # Unchanged
        assert result.description == "Updated description"  # Changed

    def test_update_not_found(self, db_session_fixture: Session):
        """Test updating a non-existent Key."""
        update_data = KeyUpdate(description="Updated description")
        result = KeyCRUD.update(db_session_fixture, 999, update_data)
        assert result is None

    def test_delete(self, db_session_fixture: Session):
        """Test deleting a Key."""
        # Create a key
        key_data = KeyCreate(value="to_delete", description="To be deleted")
        created_key = KeyCRUD.create(db_session_fixture, key_data)

        # Delete it
        result = KeyCRUD.delete(db_session_fixture, created_key.id)
        assert result is True

        # Verify it's gone
        deleted_key = KeyCRUD.get(db_session_fixture, id=created_key.id)
        assert deleted_key is None

    def test_delete_not_found(self, db_session_fixture: Session):
        """Test deleting a non-existent Key."""
        result = KeyCRUD.delete(db_session_fixture, 999)
        assert result is False


class TestEntityTypeCRUD:
    def test_create(self, db_session_fixture: Session):
        """Test creating a new EntityType."""
        entity_data = EntityTypeCreate(name="server", description="Server entity type")
        result = EntityTypeCRUD.create(db_session_fixture, entity_data)

        assert result.id is not None
        assert result.name == "server"
        assert result.description == "Server entity type"

    def test_get_by_id(self, db_session_fixture: Session):
        """Test getting an EntityType by ID."""
        entity_data = EntityTypeCreate(name="client", description="Client entity type")
        created_entity = EntityTypeCRUD.create(db_session_fixture, entity_data)

        result = EntityTypeCRUD.get(db_session_fixture, id=created_entity.id)

        assert result is not None
        assert isinstance(result, EntityType)
        assert result.id == created_entity.id
        assert result.name == "client"

    def test_get_by_id_not_found(self, db_session_fixture: Session):
        """Test getting an EntityType by non-existent ID."""
        result = EntityTypeCRUD.get(db_session_fixture, id=999)
        assert result is None

    def test_get_all(self, db_session_fixture: Session):
        """Test getting all EntityTypes."""
        entity1_data = EntityTypeCreate(name="server", description="Server type")
        entity2_data = EntityTypeCreate(name="client", description="Client type")

        EntityTypeCRUD.create(db_session_fixture, entity1_data)
        EntityTypeCRUD.create(db_session_fixture, entity2_data)

        result = EntityTypeCRUD.get(db_session_fixture)

        assert isinstance(result, list)
        assert len(result) == 2
        assert any(entity.name == "server" for entity in result)
        assert any(entity.name == "client" for entity in result)

    def test_get_with_filters(self, db_session_fixture: Session):
        """Test getting EntityTypes with filters."""
        entity1_data = EntityTypeCreate(name="server", description="Server type")
        entity2_data = EntityTypeCreate(name="client", description="Client type")

        EntityTypeCRUD.create(db_session_fixture, entity1_data)
        EntityTypeCRUD.create(db_session_fixture, entity2_data)

        result = EntityTypeCRUD.get(db_session_fixture, name="server")

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].name == "server"

    def test_update(self, db_session_fixture: Session):
        """Test updating an EntityType."""
        entity_data = EntityTypeCreate(
            name="server", description="Original description"
        )
        created_entity = EntityTypeCRUD.create(db_session_fixture, entity_data)

        update_data = EntityTypeUpdate(description="Updated description")
        result = EntityTypeCRUD.update(
            db_session_fixture, created_entity.id, update_data
        )

        assert result is not None
        assert result.name == "server"  # Unchanged
        assert result.description == "Updated description"  # Changed

    def test_update_not_found(self, db_session_fixture: Session):
        """Test updating a non-existent EntityType."""
        update_data = EntityTypeUpdate(description="Updated description")
        result = EntityTypeCRUD.update(db_session_fixture, 999, update_data)
        assert result is None

    def test_delete(self, db_session_fixture: Session):
        """Test deleting an EntityType."""
        entity_data = EntityTypeCreate(name="to_delete", description="To be deleted")
        created_entity = EntityTypeCRUD.create(db_session_fixture, entity_data)

        result = EntityTypeCRUD.delete(db_session_fixture, created_entity.id)
        assert result is True

        deleted_entity = EntityTypeCRUD.get(db_session_fixture, id=created_entity.id)
        assert deleted_entity is None

    def test_delete_not_found(self, db_session_fixture: Session):
        """Test deleting a non-existent EntityType."""
        result = EntityTypeCRUD.delete(db_session_fixture, 999)
        assert result is False


class TestDeviceClassCRUD:
    def test_create(self, db_session_fixture: Session):
        """Test creating a new DeviceClass."""
        device_data = DeviceClassCreate(
            name="BESS", description="Battery Energy Storage System"
        )
        result = DeviceClassCRUD.create(db_session_fixture, device_data)

        assert result.id is not None
        assert result.name == "BESS"
        assert result.description == "Battery Energy Storage System"
        assert result.created_at is not None

    def test_get_by_id(self, db_session_fixture: Session):
        """Test getting a DeviceClass by ID."""
        device_data = DeviceClassCreate(name="inverter", description="Power inverter")
        created_device = DeviceClassCRUD.create(db_session_fixture, device_data)

        result = DeviceClassCRUD.get(db_session_fixture, id=created_device.id)

        assert result is not None
        assert isinstance(result, DeviceClass)
        assert result.id == created_device.id
        assert result.name == "inverter"

    def test_get_by_id_not_found(self, db_session_fixture: Session):
        """Test getting a DeviceClass by non-existent ID."""
        result = DeviceClassCRUD.get(db_session_fixture, id=999)
        assert result is None

    def test_get_all(self, db_session_fixture: Session):
        """Test getting all DeviceClasses."""
        device1_data = DeviceClassCreate(name="BESS", description="Battery system")
        device2_data = DeviceClassCreate(name="inverter", description="Power inverter")

        DeviceClassCRUD.create(db_session_fixture, device1_data)
        DeviceClassCRUD.create(db_session_fixture, device2_data)

        result = DeviceClassCRUD.get(db_session_fixture)

        assert isinstance(result, list)
        assert len(result) == 2
        assert any(device.name == "BESS" for device in result)
        assert any(device.name == "inverter" for device in result)

    def test_get_with_filters(self, db_session_fixture: Session):
        """Test getting DeviceClasses with filters."""
        device1_data = DeviceClassCreate(name="BESS", description="Battery system")
        device2_data = DeviceClassCreate(name="inverter", description="Power inverter")

        DeviceClassCRUD.create(db_session_fixture, device1_data)
        DeviceClassCRUD.create(db_session_fixture, device2_data)

        result = DeviceClassCRUD.get(db_session_fixture, name="BESS")

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].name == "BESS"

    def test_update(self, db_session_fixture: Session):
        """Test updating a DeviceClass."""
        device_data = DeviceClassCreate(name="BESS", description="Original description")
        created_device = DeviceClassCRUD.create(db_session_fixture, device_data)

        update_data = DeviceClassUpdate(description="Updated description")
        result = DeviceClassCRUD.update(
            db_session_fixture, created_device.id, update_data
        )

        assert result is not None
        assert result.name == "BESS"  # Unchanged
        assert result.description == "Updated description"  # Changed

    def test_update_not_found(self, db_session_fixture: Session):
        """Test updating a non-existent DeviceClass."""
        update_data = DeviceClassUpdate(description="Updated description")
        result = DeviceClassCRUD.update(db_session_fixture, 999, update_data)
        assert result is None

    def test_delete(self, db_session_fixture: Session):
        """Test deleting a DeviceClass."""
        device_data = DeviceClassCreate(name="to_delete", description="To be deleted")
        created_device = DeviceClassCRUD.create(db_session_fixture, device_data)

        result = DeviceClassCRUD.delete(db_session_fixture, created_device.id)
        assert result is True

        deleted_device = DeviceClassCRUD.get(db_session_fixture, id=created_device.id)
        assert deleted_device is None

    def test_delete_not_found(self, db_session_fixture: Session):
        """Test deleting a non-existent DeviceClass."""
        result = DeviceClassCRUD.delete(db_session_fixture, 999)
        assert result is False


class TestListingCRUD:
    @pytest.fixture
    def entity_type(self, db_session_fixture: Session):
        """Create an EntityType for testing Listings."""
        entity_data = EntityTypeCreate(name="server", description="Server type")
        return EntityTypeCRUD.create(db_session_fixture, entity_data)

    def test_create(self, db_session_fixture: Session, entity_type: EntityType):
        """Test creating a new Listing."""
        listing_data = ListingCreate(
            entity_type_id=entity_type.id,
            manufacturer="Tesla",
            model="Powerwall",
            status=StatusEnum.active,
        )
        result = ListingCRUD.create(db_session_fixture, listing_data)

        assert result.id is not None
        assert result.entity_type_id == entity_type.id
        assert result.manufacturer == "Tesla"
        assert result.model == "Powerwall"
        assert result.status == "active"
        assert result.created_at is not None
        assert result.updated_at is not None

    def test_get_by_id(self, db_session_fixture: Session, entity_type: EntityType):
        """Test getting a Listing by ID."""
        listing_data = ListingCreate(
            entity_type_id=entity_type.id, manufacturer="BYD", model="Blade Battery"
        )
        created_listing = ListingCRUD.create(db_session_fixture, listing_data)

        result = ListingCRUD.get(db_session_fixture, id=created_listing.id)

        assert result is not None
        assert isinstance(result, Listing)
        assert result.id == created_listing.id
        assert result.manufacturer == "BYD"
        assert result.model == "Blade Battery"

    def test_get_by_id_not_found(self, db_session_fixture: Session):
        """Test getting a Listing by non-existent ID."""
        result = ListingCRUD.get(db_session_fixture, id=999)
        assert result is None

    def test_get_all(self, db_session_fixture: Session, entity_type: EntityType):
        """Test getting all Listings."""
        listing1_data = ListingCreate(
            entity_type_id=entity_type.id, manufacturer="Tesla", model="Powerwall"
        )
        listing2_data = ListingCreate(
            entity_type_id=entity_type.id, manufacturer="BYD", model="Blade Battery"
        )

        ListingCRUD.create(db_session_fixture, listing1_data)
        ListingCRUD.create(db_session_fixture, listing2_data)

        result = ListingCRUD.get(db_session_fixture)

        assert isinstance(result, list)
        assert len(result) == 2
        assert any(listing.manufacturer == "Tesla" for listing in result)
        assert any(listing.manufacturer == "BYD" for listing in result)

    def test_get_with_filters(
        self, db_session_fixture: Session, entity_type: EntityType
    ):
        """Test getting Listings with filters."""
        listing1_data = ListingCreate(
            entity_type_id=entity_type.id,
            manufacturer="Tesla",
            model="Powerwall",
            status=StatusEnum.active,
        )
        listing2_data = ListingCreate(
            entity_type_id=entity_type.id,
            manufacturer="Tesla",
            model="Solar Roof",
            status=StatusEnum.suspended,
        )

        ListingCRUD.create(db_session_fixture, listing1_data)
        ListingCRUD.create(db_session_fixture, listing2_data)

        # Filter by manufacturer
        result = ListingCRUD.get(db_session_fixture, manufacturer="Tesla")
        assert isinstance(result, list)
        assert len(result) == 2

        # Filter by status
        result = ListingCRUD.get(db_session_fixture, status="active")
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].model == "Powerwall"

    def test_update(self, db_session_fixture: Session, entity_type: EntityType):
        """Test updating a Listing."""
        listing_data = ListingCreate(
            entity_type_id=entity_type.id,
            manufacturer="Tesla",
            model="Powerwall",
            status=StatusEnum.active,
        )
        created_listing = ListingCRUD.create(db_session_fixture, listing_data)

        update_data = ListingUpdate(status=StatusEnum.suspended)
        result = ListingCRUD.update(db_session_fixture, created_listing.id, update_data)

        assert result is not None
        assert result.manufacturer == "Tesla"  # Unchanged
        assert result.status == "suspended"  # Changed

    def test_update_not_found(self, db_session_fixture: Session):
        """Test updating a non-existent Listing."""
        update_data = ListingUpdate(status=StatusEnum.suspended)
        result = ListingCRUD.update(db_session_fixture, 999, update_data)
        assert result is None

    def test_delete(self, db_session_fixture: Session, entity_type: EntityType):
        """Test deleting a Listing."""
        listing_data = ListingCreate(
            entity_type_id=entity_type.id, manufacturer="ToDelete", model="Model"
        )
        created_listing = ListingCRUD.create(db_session_fixture, listing_data)

        result = ListingCRUD.delete(db_session_fixture, created_listing.id)
        assert result is True

        deleted_listing = ListingCRUD.get(db_session_fixture, id=created_listing.id)
        assert deleted_listing is None

    def test_delete_not_found(self, db_session_fixture: Session):
        """Test deleting a non-existent Listing."""
        result = ListingCRUD.delete(db_session_fixture, 999)
        assert result is False


class TestListingDeviceClassCRUD:
    @pytest.fixture
    def setup_data(self, db_session_fixture: Session):
        """Create required EntityType, DeviceClass, and Listing for testing."""
        entity_type_data = EntityTypeCreate(name="server", description="Server type")
        entity_type = EntityTypeCRUD.create(db_session_fixture, entity_type_data)

        device_class_data = DeviceClassCreate(name="BESS", description="Battery system")
        device_class = DeviceClassCRUD.create(db_session_fixture, device_class_data)

        listing_data = ListingCreate(
            entity_type_id=entity_type.id, manufacturer="Tesla", model="Powerwall"
        )
        listing = ListingCRUD.create(db_session_fixture, listing_data)

        return {
            "entity_type": entity_type,
            "device_class": device_class,
            "listing": listing,
        }

    def test_create(
        self, db_session_fixture: Session, setup_data: dict[str, HasIdProtocol]
    ):
        """Test creating a new ListingDeviceClass."""
        ldc_data = ListingDeviceClassCreate(
            listing_id=setup_data["listing"].id,
            device_class_id=setup_data["device_class"].id,
        )
        result = ListingDeviceClassCRUD.create(db_session_fixture, ldc_data)

        assert result.id is not None
        assert result.listing_id == setup_data["listing"].id
        assert result.device_class_id == setup_data["device_class"].id
        assert result.created_at is not None

    def test_get_by_id(
        self, db_session_fixture: Session, setup_data: dict[str, HasIdProtocol]
    ):
        """Test getting a ListingDeviceClass by ID."""
        ldc_data = ListingDeviceClassCreate(
            listing_id=setup_data["listing"].id,
            device_class_id=setup_data["device_class"].id,
        )
        created_ldc = ListingDeviceClassCRUD.create(db_session_fixture, ldc_data)

        result = ListingDeviceClassCRUD.get(db_session_fixture, id=created_ldc.id)

        assert result is not None
        assert isinstance(result, ListingDeviceClass)
        assert result.id == created_ldc.id
        assert result.listing_id == setup_data["listing"].id

    def test_get_with_filters(
        self, db_session_fixture: Session, setup_data: dict[str, HasIdProtocol]
    ):
        """Test getting ListingDeviceClass with filters."""
        ldc_data = ListingDeviceClassCreate(
            listing_id=setup_data["listing"].id,
            device_class_id=setup_data["device_class"].id,
        )
        ListingDeviceClassCRUD.create(db_session_fixture, ldc_data)

        result = ListingDeviceClassCRUD.get(
            db_session_fixture, listing_id=setup_data["listing"].id
        )

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].listing_id == setup_data["listing"].id

    def test_delete(
        self, db_session_fixture: Session, setup_data: dict[str, HasIdProtocol]
    ):
        """Test deleting a ListingDeviceClass."""
        ldc_data = ListingDeviceClassCreate(
            listing_id=setup_data["listing"].id,
            device_class_id=setup_data["device_class"].id,
        )
        created_ldc = ListingDeviceClassCRUD.create(db_session_fixture, ldc_data)

        result = ListingDeviceClassCRUD.delete(db_session_fixture, created_ldc.id)
        assert result is True

        deleted_ldc = ListingDeviceClassCRUD.get(db_session_fixture, id=created_ldc.id)
        assert deleted_ldc is None


class TestDeviceClassAttributeCRUD:
    @pytest.fixture
    def device_class(self, db_session_fixture: Session):
        """Create a DeviceClass for testing attributes."""
        device_data = DeviceClassCreate(name="BESS", description="Battery system")
        return DeviceClassCRUD.create(db_session_fixture, device_data)

    def test_create(self, db_session_fixture: Session, device_class: DeviceClass):
        """Test creating a new DeviceClassAttribute."""
        attr_data = DeviceClassAttributeCreate(
            device_class_id=device_class.id,
            attribute_name="capacity",
            attribute_type=AttributeTypeEnum.number,
            description="Battery capacity in kWh",
        )
        result = DeviceClassAttributeCRUD.create(db_session_fixture, attr_data)

        assert result.id is not None
        assert result.device_class_id == device_class.id
        assert result.attribute_name == "capacity"
        assert result.attribute_type == "number"
        assert result.description == "Battery capacity in kWh"

    def test_get_by_id(self, db_session_fixture: Session, device_class: DeviceClass):
        """Test getting a DeviceClassAttribute by ID."""
        attr_data = DeviceClassAttributeCreate(
            device_class_id=device_class.id,
            attribute_name="voltage",
            attribute_type=AttributeTypeEnum.number,
        )
        created_attr = DeviceClassAttributeCRUD.create(db_session_fixture, attr_data)

        result = DeviceClassAttributeCRUD.get(db_session_fixture, id=created_attr.id)

        assert result is not None
        assert isinstance(result, DeviceClassAttribute)
        assert result.id == created_attr.id
        assert result.attribute_name == "voltage"

    def test_get_with_filters(
        self, db_session_fixture: Session, device_class: DeviceClass
    ):
        """Test getting DeviceClassAttributes with filters."""
        attr1_data = DeviceClassAttributeCreate(
            device_class_id=device_class.id,
            attribute_name="capacity",
            attribute_type=AttributeTypeEnum.number,
        )
        attr2_data = DeviceClassAttributeCreate(
            device_class_id=device_class.id,
            attribute_name="color",
            attribute_type=AttributeTypeEnum.string,
        )

        DeviceClassAttributeCRUD.create(db_session_fixture, attr1_data)
        DeviceClassAttributeCRUD.create(db_session_fixture, attr2_data)

        result = DeviceClassAttributeCRUD.get(
            db_session_fixture, device_class_id=device_class.id, attribute_type="number"
        )

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].attribute_name == "capacity"

    def test_update(self, db_session_fixture: Session, device_class: DeviceClass):
        """Test updating a DeviceClassAttribute."""
        attr_data = DeviceClassAttributeCreate(
            device_class_id=device_class.id,
            attribute_name="capacity",
            attribute_type=AttributeTypeEnum.number,
            description="Original description",
        )
        created_attr = DeviceClassAttributeCRUD.create(db_session_fixture, attr_data)

        update_data = DeviceClassAttributeUpdate(description="Updated description")
        result = DeviceClassAttributeCRUD.update(
            db_session_fixture, created_attr.id, update_data
        )

        assert result is not None
        assert result.attribute_name == "capacity"  # Unchanged
        assert result.description == "Updated description"  # Changed

    def test_delete(self, db_session_fixture: Session, device_class: DeviceClass):
        """Test deleting a DeviceClassAttribute."""
        attr_data = DeviceClassAttributeCreate(
            device_class_id=device_class.id,
            attribute_name="to_delete",
            attribute_type=AttributeTypeEnum.string,
        )
        created_attr = DeviceClassAttributeCRUD.create(db_session_fixture, attr_data)

        result = DeviceClassAttributeCRUD.delete(db_session_fixture, created_attr.id)
        assert result is True

        deleted_attr = DeviceClassAttributeCRUD.get(
            db_session_fixture, id=created_attr.id
        )
        assert deleted_attr is None


class TestListingDeviceClassAttributeCRUD:
    @pytest.fixture
    def setup_data(self, db_session_fixture: Session):
        """Create required data for testing ListingDeviceClassAttribute."""
        entity_type_data = EntityTypeCreate(name="server", description="Server type")
        entity_type = EntityTypeCRUD.create(db_session_fixture, entity_type_data)

        device_class_data = DeviceClassCreate(name="BESS", description="Battery system")
        device_class = DeviceClassCRUD.create(db_session_fixture, device_class_data)

        listing_data = ListingCreate(
            entity_type_id=entity_type.id, manufacturer="Tesla", model="Powerwall"
        )
        listing = ListingCRUD.create(db_session_fixture, listing_data)

        return {
            "entity_type": entity_type,
            "device_class": device_class,
            "listing": listing,
        }

    def test_create(
        self, db_session_fixture: Session, setup_data: dict[str, HasIdProtocol]
    ):
        """Test creating a new ListingDeviceClassAttribute."""
        attr_data = ListingDeviceClassAttributeCreate(
            listing_id=setup_data["listing"].id,
            device_class_id=setup_data["device_class"].id,
            attribute_name="capacity",
            attribute_value="13.5",
        )
        result = ListingDeviceClassAttributeCRUD.create(db_session_fixture, attr_data)

        assert result.id is not None
        assert result.listing_id == setup_data["listing"].id
        assert result.device_class_id == setup_data["device_class"].id
        assert result.attribute_name == "capacity"
        assert result.attribute_value == "13.5"
        assert result.created_at is not None

    def test_get_by_id(
        self, db_session_fixture: Session, setup_data: dict[str, HasIdProtocol]
    ):
        """Test getting a ListingDeviceClassAttribute by ID."""
        attr_data = ListingDeviceClassAttributeCreate(
            listing_id=setup_data["listing"].id,
            device_class_id=setup_data["device_class"].id,
            attribute_name="voltage",
            attribute_value="400V",
        )
        created_attr = ListingDeviceClassAttributeCRUD.create(
            db_session_fixture, attr_data
        )

        result = ListingDeviceClassAttributeCRUD.get(
            db_session_fixture, id=created_attr.id
        )

        assert result is not None
        assert isinstance(result, ListingDeviceClassAttribute)
        assert result.id == created_attr.id
        assert result.attribute_name == "voltage"
        assert result.attribute_value == "400V"

    def test_get_with_filters(
        self, db_session_fixture: Session, setup_data: dict[str, HasIdProtocol]
    ):
        """Test getting ListingDeviceClassAttributes with filters."""
        attr1_data = ListingDeviceClassAttributeCreate(
            listing_id=setup_data["listing"].id,
            device_class_id=setup_data["device_class"].id,
            attribute_name="capacity",
            attribute_value="13.5",
        )
        attr2_data = ListingDeviceClassAttributeCreate(
            listing_id=setup_data["listing"].id,
            device_class_id=setup_data["device_class"].id,
            attribute_name="voltage",
            attribute_value="400V",
        )

        ListingDeviceClassAttributeCRUD.create(db_session_fixture, attr1_data)
        ListingDeviceClassAttributeCRUD.create(db_session_fixture, attr2_data)

        result = ListingDeviceClassAttributeCRUD.get(
            db_session_fixture,
            listing_id=setup_data["listing"].id,
            attribute_name="capacity",
        )

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].attribute_name == "capacity"
        assert result[0].attribute_value == "13.5"

    def test_update(
        self, db_session_fixture: Session, setup_data: dict[str, HasIdProtocol]
    ):
        """Test updating a ListingDeviceClassAttribute."""
        attr_data = ListingDeviceClassAttributeCreate(
            listing_id=setup_data["listing"].id,
            device_class_id=setup_data["device_class"].id,
            attribute_name="capacity",
            attribute_value="13.5",
        )
        created_attr = ListingDeviceClassAttributeCRUD.create(
            db_session_fixture, attr_data
        )

        update_data = ListingDeviceClassAttributeUpdate(attribute_value="15.0")
        result = ListingDeviceClassAttributeCRUD.update(
            db_session_fixture, created_attr.id, update_data
        )

        assert result is not None
        assert result.attribute_name == "capacity"  # Unchanged
        assert result.attribute_value == "15.0"  # Changed

    def test_delete(
        self, db_session_fixture: Session, setup_data: dict[str, HasIdProtocol]
    ):
        """Test deleting a ListingDeviceClassAttribute."""
        attr_data = ListingDeviceClassAttributeCreate(
            listing_id=setup_data["listing"].id,
            device_class_id=setup_data["device_class"].id,
            attribute_name="to_delete",
            attribute_value="delete_me",
        )
        created_attr = ListingDeviceClassAttributeCRUD.create(
            db_session_fixture, attr_data
        )

        result = ListingDeviceClassAttributeCRUD.delete(
            db_session_fixture, created_attr.id
        )
        assert result is True

        deleted_attr = ListingDeviceClassAttributeCRUD.get(
            db_session_fixture, id=created_attr.id
        )
        assert deleted_attr is None


class TestCertificateCRUD:
    @pytest.fixture
    def setup_data(self, db_session_fixture: Session):
        """Create required data for testing Certificate."""
        entity_type_data = EntityTypeCreate(name="server", description="Server type")
        entity_type = EntityTypeCRUD.create(db_session_fixture, entity_type_data)

        listing_data = ListingCreate(
            entity_type_id=entity_type.id, manufacturer="Tesla", model="Powerwall"
        )
        listing = ListingCRUD.create(db_session_fixture, listing_data)

        return {"entity_type": entity_type, "listing": listing}

    def test_create(
        self, db_session_fixture: Session, setup_data: dict[str, HasIdProtocol]
    ):
        """Test creating a new Certificate."""
        cert_data = CertificateCreate(
            listing_id=setup_data["listing"].id,
            expiry=date(2025, 12, 31),
            certification_date=date(2024, 1, 1),
            certifying_body="UL",
            test_profiles=["AS4777", "IEEE1547"],
        )
        result = CertificateCRUD.create(db_session_fixture, cert_data)

        assert result.id is not None
        assert result.listing_id == setup_data["listing"].id
        assert result.expiry == date(2025, 12, 31)
        assert result.certification_date == date(2024, 1, 1)
        assert result.certifying_body == "UL"
        assert result.test_profiles == ["AS4777", "IEEE1547"]

    def test_get_by_id(
        self, db_session_fixture: Session, setup_data: dict[str, HasIdProtocol]
    ):
        """Test getting a Certificate by ID."""
        cert_data = CertificateCreate(
            listing_id=setup_data["listing"].id,
            expiry=date(2025, 6, 30),
            certification_date=date(2024, 6, 30),
            certifying_body="TUV",
            test_profiles=["IEC61215"],
        )
        created_cert = CertificateCRUD.create(db_session_fixture, cert_data)

        result = CertificateCRUD.get(db_session_fixture, id=created_cert.id)

        assert result is not None
        assert isinstance(result, Certificate)
        assert result.id == created_cert.id
        assert result.certifying_body == "TUV"
        assert result.test_profiles == ["IEC61215"]

    def test_get_by_id_not_found(self, db_session_fixture: Session):
        """Test getting a Certificate by non-existent ID."""
        result = CertificateCRUD.get(db_session_fixture, id=999)
        assert result is None

    def test_get_all(
        self, db_session_fixture: Session, setup_data: dict[str, HasIdProtocol]
    ):
        """Test getting all Certificates."""
        cert1_data = CertificateCreate(
            listing_id=setup_data["listing"].id,
            expiry=date(2025, 12, 31),
            certification_date=date(2024, 1, 1),
            certifying_body="UL",
            test_profiles=["AS4777"],
        )
        cert2_data = CertificateCreate(
            listing_id=setup_data["listing"].id,
            expiry=date(2024, 12, 31),
            certification_date=date(2023, 1, 1),
            certifying_body="TUV",
            test_profiles=["IEC61215"],
        )

        CertificateCRUD.create(db_session_fixture, cert1_data)
        CertificateCRUD.create(db_session_fixture, cert2_data)

        result = CertificateCRUD.get(db_session_fixture)

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 2
        assert any(cert.certifying_body == "UL" for cert in result)
        assert any(cert.certifying_body == "TUV" for cert in result)

    def test_get_with_filters(
        self, db_session_fixture: Session, setup_data: dict[str, HasIdProtocol]
    ):
        """Test getting Certificates with filters."""
        cert1_data = CertificateCreate(
            listing_id=setup_data["listing"].id,
            expiry=date(2025, 12, 31),
            certification_date=date(2024, 1, 1),
            certifying_body="UL",
            test_profiles=["AS4777"],
        )
        cert2_data = CertificateCreate(
            listing_id=setup_data["listing"].id,
            expiry=date(2024, 12, 31),
            certification_date=date(2023, 1, 1),
            certifying_body="TUV",
            test_profiles=["IEC61215"],
        )

        CertificateCRUD.create(db_session_fixture, cert1_data)
        CertificateCRUD.create(db_session_fixture, cert2_data)

        # Filter by certifying body
        result = CertificateCRUD.get(db_session_fixture, certifying_body="UL")
        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].certifying_body == "UL"

        # Filter by listing_id
        result = CertificateCRUD.get(
            db_session_fixture, listing_id=setup_data["listing"].id
        )
        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 2

        # Filter by expiry date (certificates expiring after given date)
        result = CertificateCRUD.get(db_session_fixture, expiry=date(2025, 1, 1))
        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].expiry == date(2025, 12, 31)

    def test_update(
        self, db_session_fixture: Session, setup_data: dict[str, HasIdProtocol]
    ):
        """Test updating a Certificate."""
        cert_data = CertificateCreate(
            listing_id=setup_data["listing"].id,
            expiry=date(2025, 12, 31),
            certification_date=date(2024, 1, 1),
            certifying_body="UL",
            test_profiles=["AS4777"],
        )
        created_cert = CertificateCRUD.create(db_session_fixture, cert_data)

        update_data = CertificateUpdate(
            expiry=date(2026, 12, 31), test_profiles=["AS4777", "IEEE1547"]
        )
        result = CertificateCRUD.update(
            db_session_fixture, created_cert.id, update_data
        )

        assert result is not None
        assert result.certifying_body == "UL"  # Unchanged
        assert result.expiry == date(2026, 12, 31)  # Changed
        assert result.test_profiles == ["AS4777", "IEEE1547"]  # Changed

    def test_update_not_found(self, db_session_fixture: Session):
        """Test updating a non-existent Certificate."""
        update_data = CertificateUpdate(expiry=date(2026, 12, 31))
        result = CertificateCRUD.update(db_session_fixture, 999, update_data)
        assert result is None

    def test_delete(
        self, db_session_fixture: Session, setup_data: dict[str, HasIdProtocol]
    ):
        """Test deleting a Certificate."""
        cert_data = CertificateCreate(
            listing_id=setup_data["listing"].id,
            expiry=date(2025, 12, 31),
            certification_date=date(2024, 1, 1),
            certifying_body="ToDelete",
            test_profiles=["TEST"],
        )
        created_cert = CertificateCRUD.create(db_session_fixture, cert_data)

        result = CertificateCRUD.delete(db_session_fixture, created_cert.id)
        assert result is True

        deleted_cert = CertificateCRUD.get(db_session_fixture, id=created_cert.id)
        assert deleted_cert is None

    def test_delete_not_found(self, db_session_fixture: Session):
        """Test deleting a non-existent Certificate."""
        result = CertificateCRUD.delete(db_session_fixture, 999)
        assert result is False

    def test_get_with_test_profiles_filter(
        self, db_session_fixture: Session, setup_data: dict[str, HasIdProtocol]
    ):
        """Test filtering certificates by test profiles (PostgreSQL array contains)."""
        cert1_data = CertificateCreate(
            listing_id=setup_data["listing"].id,
            expiry=date(2025, 12, 31),
            certification_date=date(2024, 1, 1),
            certifying_body="UL",
            test_profiles=["AS4777", "IEEE1547"],
        )
        cert2_data = CertificateCreate(
            listing_id=setup_data["listing"].id,
            expiry=date(2024, 12, 31),
            certification_date=date(2023, 1, 1),
            certifying_body="TUV",
            test_profiles=["IEC61215", "IEC61730"],
        )

        CertificateCRUD.create(db_session_fixture, cert1_data)
        CertificateCRUD.create(db_session_fixture, cert2_data)

        # Filter by test profiles - should find certificates containing the specified profile
        result = CertificateCRUD.get(db_session_fixture, test_profiles=["AS4777"])
        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].certifying_body == "UL"
        assert "AS4777" in result[0].test_profiles
