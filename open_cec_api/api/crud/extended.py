from __future__ import annotations

from typing import Any, Dict

from open_cec_api.services.database.models import Listing

# TODO define some extended model type,
# make this return that model type and define or update the router endpoint to use
# that model type as that response_model


def listing_to_detail_dict(listing: Listing) -> Dict[str, Any]:
    """
    Optional helper to shape a detailed JSON-ready payload (more explicit than returning ORM objects).
    """
    return {
        "id": listing.id,
        "manufacturer": listing.manufacturer,
        "model": listing.model,
        "status": listing.status,
        "created_at": listing.created_at.isoformat() if listing.created_at else None,
        "updated_at": listing.updated_at.isoformat() if listing.updated_at else None,
        "entity_type": listing.entity_type.name if listing.entity_type else None,
        "device_classes": [
            {
                "listing_device_class_id": ldc.id,
                "device_class": {
                    "id": ldc.device_class.id,
                    "name": ldc.device_class.name,
                    "description": ldc.device_class.description,
                    "created_at": ldc.device_class.created_at.isoformat()
                    if ldc.device_class.created_at
                    else None,
                    "attributes": [
                        {
                            "id": a.id,
                            "attribute_name": a.attribute_name,
                            "attribute_type": a.attribute_type,
                            "description": a.description,
                        }
                        for a in (ldc.device_class.device_class_attributes or [])
                    ],
                }
                if ldc.device_class
                else None,
                # "created_at": ldc.created_at.isoformat() if ldc.created_at else None,
            }
            for ldc in (listing.listing_device_classes or [])
        ],
        "listing_device_class_attributes": [
            {
                "id": a.id,
                "listing_id": a.listing_id,
                "device_class_id": a.device_class_id,
                "attribute_name": a.attribute_name,
                "attribute_value": a.attribute_value,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            }
            for a in (listing.listing_device_class_attributes or [])
        ],
        "certificates": [
            {
                "id": c.id,
                "listing_id": c.listing_id,
                "expiry": c.expiry.isoformat() if c.expiry else None,
                "certification_date": c.certification_date.isoformat()
                if c.certification_date
                else None,
                "certifying_body": c.certifying_body,
                "test_profiles": list(c.test_profiles or []),
            }
            for c in (listing.certificates or [])
        ],
    }
