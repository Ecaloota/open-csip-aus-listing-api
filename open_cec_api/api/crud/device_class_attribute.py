from typing import List, Optional, Union

from sqlalchemy.orm import Session

from open_cec_api.api.crud.base import CRUDClass
from open_cec_api.api.schema.create import DeviceClassAttributeCreate
from open_cec_api.api.schema.update import DeviceClassAttributeUpdate
from open_cec_api.services.database.models import DeviceClassAttribute


class DeviceClassAttributeCRUD(CRUDClass[DeviceClassAttribute]):
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
