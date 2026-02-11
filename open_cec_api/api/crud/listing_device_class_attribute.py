from typing import List, Optional, Union

from sqlalchemy.orm import Session

from open_cec_api.api.crud.base import CRUDClass
from open_cec_api.api.schema.create import ListingDeviceClassAttributeCreate
from open_cec_api.api.schema.update import ListingDeviceClassAttributeUpdate
from open_cec_api.services.database.models import ListingDeviceClassAttribute


class ListingDeviceClassAttributeCRUD(CRUDClass[ListingDeviceClassAttribute]):
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
