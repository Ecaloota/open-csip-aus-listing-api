from typing import List, Optional, Union

from sqlalchemy.orm import Session

from open_cec_api.api.crud.base import CRUDClass
from open_cec_api.api.schema.create import KeyCreate
from open_cec_api.api.schema.update import KeyUpdate
from open_cec_api.services.database.models import Key


class KeyCRUD(CRUDClass[Key]):
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
