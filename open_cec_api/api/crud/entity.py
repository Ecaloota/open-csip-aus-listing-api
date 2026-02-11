from typing import List, Optional, Union

from sqlalchemy.orm import Session

from open_cec_api.api.crud.base import CRUDClass
from open_cec_api.api.schema.create import EntityTypeCreate
from open_cec_api.api.schema.update import EntityTypeUpdate
from open_cec_api.services.database.models import EntityType


class EntityTypeCRUD(CRUDClass[EntityType]):
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
