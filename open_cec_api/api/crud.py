from typing import List, Optional, Union

from sqlalchemy.orm import Session

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


class KeyCRUD:
    @staticmethod
    def get(
        session: Session, id: Optional[int] = None, **filters
    ) -> Union[Key, List[Key], None]:
        """
        Get Key(s) by ID or filters.

        Args:
            session: Database session
            id: Primary key ID (if provided, returns single record)
            **filters: Filter conditions (value, description)

        Returns:
            Single Key if id provided, List[Key] if filters provided, or None if not found
        """
        query = session.query(Key)

        if id is not None:
            return query.filter(Key.id == id).first()

        # Apply filters
        if "value" in filters:
            query = query.filter(Key.value == filters["value"])
        if "description" in filters:
            query = query.filter(Key.description.ilike(f"%{filters['description']}%"))

        return query.all()

    @staticmethod
    def create(session: Session, key_data: KeyCreate) -> Key:
        """Create a new Key from Pydantic model."""
        key = Key(**key_data.model_dump())
        session.add(key)
        session.commit()
        session.refresh(key)
        return key

    @staticmethod
    def update(session: Session, id: int, key_data: KeyUpdate) -> Optional[Key]:
        """Update a Key by ID using Pydantic model."""
        key = session.query(Key).filter(Key.id == id).first()
        if key:
            update_data = key_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(key, field):
                    setattr(key, field, value)
            session.commit()
            session.refresh(key)
        return key

    @staticmethod
    def delete(session: Session, id: int) -> bool:
        """Delete a Key by ID. Returns True if deleted, False if not found."""
        key = session.query(Key).filter(Key.id == id).first()
        if key:
            session.delete(key)
            session.commit()
            return True
        return False


class EntityTypeCRUD:
    @staticmethod
    def get(
        session: Session, id: Optional[int] = None, **filters
    ) -> Union[EntityType, List[EntityType], None]:
        """
        Get EntityType(s) by ID or filters.

        Args:
            session: Database session
            id: Primary key ID
            **filters: Filter conditions (name, description)
        """
        query = session.query(EntityType)

        if id is not None:
            return query.filter(EntityType.id == id).first()

        # Apply filters
        if "name" in filters:
            query = query.filter(EntityType.name == filters["name"])
        if "description" in filters:
            query = query.filter(
                EntityType.description.ilike(f"%{filters['description']}%")
            )

        return query.all()

    @staticmethod
    def create(session: Session, entity_type_data: EntityTypeCreate) -> EntityType:
        """Create a new EntityType from Pydantic model."""
        entity_type = EntityType(**entity_type_data.model_dump())
        session.add(entity_type)
        session.commit()
        session.refresh(entity_type)
        return entity_type

    @staticmethod
    def update(
        session: Session, id: int, entity_type_data: EntityTypeUpdate
    ) -> Optional[EntityType]:
        """Update an EntityType by ID using Pydantic model."""
        entity_type = session.query(EntityType).filter(EntityType.id == id).first()
        if entity_type:
            update_data = entity_type_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(entity_type, field):
                    setattr(entity_type, field, value)
            session.commit()
            session.refresh(entity_type)
        return entity_type

    @staticmethod
    def delete(session: Session, id: int) -> bool:
        """Delete an EntityType by ID."""
        entity_type = session.query(EntityType).filter(EntityType.id == id).first()
        if entity_type:
            session.delete(entity_type)
            session.commit()
            return True
        return False


class DeviceClassCRUD:
    @staticmethod
    def get(
        session: Session, id: Optional[int] = None, **filters
    ) -> Union[DeviceClass, List[DeviceClass], None]:
        """
        Get DeviceClass(es) by ID or filters.

        Args:
            session: Database session
            id: Primary key ID
            **filters: Filter conditions (name, description, created_at)
        """
        query = session.query(DeviceClass)

        if id is not None:
            return query.filter(DeviceClass.id == id).first()

        # Apply filters
        if "name" in filters:
            query = query.filter(DeviceClass.name == filters["name"])
        if "description" in filters:
            query = query.filter(
                DeviceClass.description.ilike(f"%{filters['description']}%")
            )
        if "created_at" in filters:
            query = query.filter(DeviceClass.created_at >= filters["created_at"])

        return query.all()

    @staticmethod
    def create(session: Session, device_class_data: DeviceClassCreate) -> DeviceClass:
        """Create a new DeviceClass from Pydantic model."""
        device_class = DeviceClass(**device_class_data.model_dump())
        session.add(device_class)
        session.commit()
        session.refresh(device_class)
        return device_class

    @staticmethod
    def update(
        session: Session, id: int, device_class_data: DeviceClassUpdate
    ) -> Optional[DeviceClass]:
        """Update a DeviceClass by ID using Pydantic model."""
        device_class = session.query(DeviceClass).filter(DeviceClass.id == id).first()
        if device_class:
            update_data = device_class_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(device_class, field):
                    setattr(device_class, field, value)
            session.commit()
            session.refresh(device_class)
        return device_class

    @staticmethod
    def delete(session: Session, id: int) -> bool:
        """Delete a DeviceClass by ID."""
        device_class = session.query(DeviceClass).filter(DeviceClass.id == id).first()
        if device_class:
            session.delete(device_class)
            session.commit()
            return True
        return False


class ListingCRUD:
    @staticmethod
    def get(
        session: Session, id: Optional[int] = None, **filters
    ) -> Union[Listing, List[Listing], None]:
        """
        Get Listing(s) by ID or filters.

        Args:
            session: Database session
            id: Primary key ID
            **filters: Filter conditions (entity_type_id, manufacturer, model, status)
        """
        query = session.query(Listing)

        if id is not None:
            return query.filter(Listing.id == id).first()

        # Apply filters
        if "entity_type_id" in filters:
            query = query.filter(Listing.entity_type_id == filters["entity_type_id"])
        if "manufacturer" in filters:
            query = query.filter(
                Listing.manufacturer.ilike(f"%{filters['manufacturer']}%")
            )
        if "model" in filters:
            query = query.filter(Listing.model.ilike(f"%{filters['model']}%"))
        if "status" in filters:
            query = query.filter(Listing.status == filters["status"])

        return query.all()

    @staticmethod
    def create(session: Session, listing_data: ListingCreate) -> Listing:
        """Create a new Listing from Pydantic model."""
        listing = Listing(**listing_data.model_dump())
        session.add(listing)
        session.commit()
        session.refresh(listing)
        return listing

    @staticmethod
    def update(
        session: Session, id: int, listing_data: ListingUpdate
    ) -> Optional[Listing]:
        """Update a Listing by ID using Pydantic model."""
        listing = session.query(Listing).filter(Listing.id == id).first()
        if listing:
            update_data = listing_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(listing, field):
                    setattr(listing, field, value)
            session.commit()
            session.refresh(listing)
        return listing

    @staticmethod
    def delete(session: Session, id: int) -> bool:
        """Delete a Listing by ID."""
        listing = session.query(Listing).filter(Listing.id == id).first()
        if listing:
            session.delete(listing)
            session.commit()
            return True
        return False


class ListingDeviceClassCRUD:
    @staticmethod
    def get(
        session: Session, id: Optional[int] = None, **filters
    ) -> Union[ListingDeviceClass, List[ListingDeviceClass], None]:
        """
        Get ListingDeviceClass(es) by ID or filters.

        Args:
            session: Database session
            id: Primary key ID
            **filters: Filter conditions (listing_id, device_class_id)
        """
        query = session.query(ListingDeviceClass)

        if id is not None:
            return query.filter(ListingDeviceClass.id == id).first()

        # Apply filters
        if "listing_id" in filters:
            query = query.filter(ListingDeviceClass.listing_id == filters["listing_id"])
        if "device_class_id" in filters:
            query = query.filter(
                ListingDeviceClass.device_class_id == filters["device_class_id"]
            )

        return query.all()

    @staticmethod
    def create(
        session: Session, listing_device_class_data: ListingDeviceClassCreate
    ) -> ListingDeviceClass:
        """Create a new ListingDeviceClass from Pydantic model."""
        listing_device_class = ListingDeviceClass(
            **listing_device_class_data.model_dump()
        )
        session.add(listing_device_class)
        session.commit()
        session.refresh(listing_device_class)
        return listing_device_class

    @staticmethod
    def delete(session: Session, id: int) -> bool:
        """Delete a ListingDeviceClass by ID."""
        listing_device_class = (
            session.query(ListingDeviceClass)
            .filter(ListingDeviceClass.id == id)
            .first()
        )
        if listing_device_class:
            session.delete(listing_device_class)
            session.commit()
            return True
        return False


class DeviceClassAttributeCRUD:
    @staticmethod
    def get(
        session: Session, id: Optional[int] = None, **filters
    ) -> Union[DeviceClassAttribute, List[DeviceClassAttribute], None]:
        """
        Get DeviceClassAttribute(s) by ID or filters.

        Args:
            session: Database session
            id: Primary key ID
            **filters: Filter conditions (device_class_id, attribute_name, attribute_type)
        """
        query = session.query(DeviceClassAttribute)

        if id is not None:
            return query.filter(DeviceClassAttribute.id == id).first()

        # Apply filters
        if "device_class_id" in filters:
            query = query.filter(
                DeviceClassAttribute.device_class_id == filters["device_class_id"]
            )
        if "attribute_name" in filters:
            query = query.filter(
                DeviceClassAttribute.attribute_name == filters["attribute_name"]
            )
        if "attribute_type" in filters:
            query = query.filter(
                DeviceClassAttribute.attribute_type == filters["attribute_type"]
            )
        if "description" in filters:
            query = query.filter(
                DeviceClassAttribute.description.ilike(f"%{filters['description']}%")
            )

        return query.all()

    @staticmethod
    def create(
        session: Session, device_class_attribute_data: DeviceClassAttributeCreate
    ) -> DeviceClassAttribute:
        """Create a new DeviceClassAttribute from Pydantic model."""
        attribute = DeviceClassAttribute(**device_class_attribute_data.model_dump())
        session.add(attribute)
        session.commit()
        session.refresh(attribute)
        return attribute

    @staticmethod
    def update(
        session: Session,
        id: int,
        device_class_attribute_data: DeviceClassAttributeUpdate,
    ) -> Optional[DeviceClassAttribute]:
        """Update a DeviceClassAttribute by ID using Pydantic model."""
        attribute = (
            session.query(DeviceClassAttribute)
            .filter(DeviceClassAttribute.id == id)
            .first()
        )
        if attribute:
            update_data = device_class_attribute_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(attribute, field):
                    setattr(attribute, field, value)
            session.commit()
            session.refresh(attribute)
        return attribute

    @staticmethod
    def delete(session: Session, id: int) -> bool:
        """Delete a DeviceClassAttribute by ID."""
        attribute = (
            session.query(DeviceClassAttribute)
            .filter(DeviceClassAttribute.id == id)
            .first()
        )
        if attribute:
            session.delete(attribute)
            session.commit()
            return True
        return False


class ListingDeviceClassAttributeCRUD:
    @staticmethod
    def get(
        session: Session, id: Optional[int] = None, **filters
    ) -> Union[ListingDeviceClassAttribute, List[ListingDeviceClassAttribute], None]:
        """
        Get ListingDeviceClassAttribute(s) by ID or filters.

        Args:
            session: Database session
            id: Primary key ID
            **filters: Filter conditions (listing_id, device_class_id, attribute_name, attribute_value)
        """
        query = session.query(ListingDeviceClassAttribute)

        if id is not None:
            return query.filter(ListingDeviceClassAttribute.id == id).first()

        # Apply filters
        if "listing_id" in filters:
            query = query.filter(
                ListingDeviceClassAttribute.listing_id == filters["listing_id"]
            )
        if "device_class_id" in filters:
            query = query.filter(
                ListingDeviceClassAttribute.device_class_id
                == filters["device_class_id"]
            )
        if "attribute_name" in filters:
            query = query.filter(
                ListingDeviceClassAttribute.attribute_name == filters["attribute_name"]
            )
        if "attribute_value" in filters:
            query = query.filter(
                ListingDeviceClassAttribute.attribute_value.ilike(
                    f"%{filters['attribute_value']}%"
                )
            )

        return query.all()

    @staticmethod
    def create(
        session: Session,
        listing_device_class_attribute_data: ListingDeviceClassAttributeCreate,
    ) -> ListingDeviceClassAttribute:
        """Create a new ListingDeviceClassAttribute from Pydantic model."""
        attribute = ListingDeviceClassAttribute(
            **listing_device_class_attribute_data.model_dump()
        )
        session.add(attribute)
        session.commit()
        session.refresh(attribute)
        return attribute

    @staticmethod
    def update(
        session: Session,
        id: int,
        listing_device_class_attribute_data: ListingDeviceClassAttributeUpdate,
    ) -> Optional[ListingDeviceClassAttribute]:
        """Update a ListingDeviceClassAttribute by ID using Pydantic model."""
        attribute = (
            session.query(ListingDeviceClassAttribute)
            .filter(ListingDeviceClassAttribute.id == id)
            .first()
        )
        if attribute:
            update_data = listing_device_class_attribute_data.model_dump(
                exclude_unset=True
            )
            for field, value in update_data.items():
                if hasattr(attribute, field):
                    setattr(attribute, field, value)
            session.commit()
            session.refresh(attribute)
        return attribute

    @staticmethod
    def delete(session: Session, id: int) -> bool:
        """Delete a ListingDeviceClassAttribute by ID."""
        attribute = (
            session.query(ListingDeviceClassAttribute)
            .filter(ListingDeviceClassAttribute.id == id)
            .first()
        )
        if attribute:
            session.delete(attribute)
            session.commit()
            return True
        return False


class CertificateCRUD:
    @staticmethod
    def get(
        session: Session, id: Optional[int] = None, **filters
    ) -> Union[Certificate, List[Certificate], None]:
        """
        Get Certificate(s) by ID or filters.

        Args:
            session: Database session
            id: Primary key ID
            **filters: Filter conditions (listing_id, expiry, certification_date, certifying_body, test_profiles)
        """
        query = session.query(Certificate)

        if id is not None:
            return query.filter(Certificate.id == id).first()

        # Apply filters
        if "listing_id" in filters:
            query = query.filter(Certificate.listing_id == filters["listing_id"])
        if "expiry" in filters:
            query = query.filter(Certificate.expiry >= filters["expiry"])
        if "certification_date" in filters:
            query = query.filter(
                Certificate.certification_date >= filters["certification_date"]
            )
        if "certifying_body" in filters:
            query = query.filter(
                Certificate.certifying_body.ilike(f"%{filters['certifying_body']}%")
            )
        if "test_profiles" in filters:
            # For array contains query - PostgreSQL specific
            query = query.filter(
                Certificate.test_profiles.contains(filters["test_profiles"])
            )

        return query.all()

    @staticmethod
    def create(session: Session, certificate_data: CertificateCreate) -> Certificate:
        """Create a new Certificate from Pydantic model."""
        certificate = Certificate(**certificate_data.model_dump())
        session.add(certificate)
        session.commit()
        session.refresh(certificate)
        return certificate

    @staticmethod
    def update(
        session: Session, id: int, certificate_data: CertificateUpdate
    ) -> Optional[Certificate]:
        """Update a Certificate by ID using Pydantic model."""
        certificate = session.query(Certificate).filter(Certificate.id == id).first()
        if certificate:
            update_data = certificate_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(certificate, field):
                    setattr(certificate, field, value)
            session.commit()
            session.refresh(certificate)
        return certificate

    @staticmethod
    def delete(session: Session, id: int) -> bool:
        """Delete a Certificate by ID."""
        certificate = session.query(Certificate).filter(Certificate.id == id).first()
        if certificate:
            session.delete(certificate)
            session.commit()
            return True
        return False
