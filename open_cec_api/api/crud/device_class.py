from typing import List, Optional, Union

from sqlalchemy.orm import Session

from open_cec_api.api.crud.base import CRUDClass
from open_cec_api.api.schema.create import DeviceClassCreate
from open_cec_api.api.schema.update import DeviceClassUpdate
from open_cec_api.services.database.models import DeviceClass


class DeviceClassCRUD(CRUDClass[DeviceClass]):
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
