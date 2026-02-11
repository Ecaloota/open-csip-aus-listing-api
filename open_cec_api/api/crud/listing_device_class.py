from typing import List, Optional, Union

from sqlalchemy.orm import Session

from open_cec_api.api.crud.base import CRUDClass
from open_cec_api.api.schema.create import ListingDeviceClassCreate
from open_cec_api.api.schema.update import ListingDeviceClassUpdate
from open_cec_api.services.database.models import ListingDeviceClass


class ListingDeviceClassCRUD(CRUDClass[ListingDeviceClass]):
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
    def update(
        session: Session, id: int, listing_device_class_data: ListingDeviceClassUpdate
    ) -> Optional[ListingDeviceClass]:
        """Update a ListingDeviceClass by ID using Pydantic model"""
        listing_device_class = (
            session.query(ListingDeviceClass)
            .filter(ListingDeviceClass.id == id)
            .first()
        )
        if listing_device_class:
            update_data = listing_device_class_data.model_dump(exclude_unset=True)
            for f, v in update_data.items():
                if hasattr(listing_device_class, f):
                    setattr(listing_device_class, f, v)
            session.commit()
            session.refresh(listing_device_class)
        return listing_device_class

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
