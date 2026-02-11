from typing import List, Optional, Union

from sqlalchemy.orm import Session

from open_cec_api.api.crud.base import CRUDClass
from open_cec_api.api.schema.create import ListingCreate
from open_cec_api.api.schema.update import ListingUpdate
from open_cec_api.services.database.models import Listing


class ListingCRUD(CRUDClass[Listing]):
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
