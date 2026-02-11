from typing import List, Optional, Union

from sqlalchemy.orm import Session

from open_cec_api.api.crud.base import CRUDClass
from open_cec_api.api.schema.create import CertificateCreate
from open_cec_api.api.schema.update import CertificateUpdate
from open_cec_api.services.database.models import Certificate


class CertificateCRUD(CRUDClass[Certificate]):
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
