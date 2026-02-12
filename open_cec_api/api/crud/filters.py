import open_cec_api.services.database.models as models

OPERATOR_MAP = {
    "eq": lambda c, v: c == v,
    "ge": lambda c, v: c >= v,
    "ilike": lambda c, v: c.ilike(f"%{v}%"),
    "in": lambda c, v: c.contains(v),
}

CLS_TO_KW_FILTERS = {
    models.DeviceClass: {
        "name": OPERATOR_MAP["eq"],
        "description": OPERATOR_MAP["ilike"],
        "created_at": OPERATOR_MAP["ge"],
    },
    models.DeviceClassAttribute: {
        "device_class_id": OPERATOR_MAP["eq"],
        "attribute_name": OPERATOR_MAP["eq"],
        "attribute_type": OPERATOR_MAP["eq"],
        "description": OPERATOR_MAP["ilike"],
    },
    models.Certificate: {
        "listing_id": OPERATOR_MAP["eq"],
        "expiry": OPERATOR_MAP["ge"],
        "certification_date": OPERATOR_MAP["ge"],
        "certifying_body": OPERATOR_MAP["ilike"],
        "test_profiles": OPERATOR_MAP["in"],
    },
    models.EntityType: {
        "name": OPERATOR_MAP["eq"],
        "description": OPERATOR_MAP["ilike"],
    },
    models.Key: {
        "value": OPERATOR_MAP["eq"],
        "description": OPERATOR_MAP["ilike"],
    },
    models.ListingDeviceClassAttribute: {
        "listing_id": OPERATOR_MAP["eq"],
        "device_class_id": OPERATOR_MAP["eq"],
        "attribute_name": OPERATOR_MAP["eq"],
        "attribute_value": OPERATOR_MAP["ilike"],
    },
    models.ListingDeviceClass: {
        "listing_id": OPERATOR_MAP["eq"],
        "device_class_id": OPERATOR_MAP["eq"],
    },
    models.Listing: {
        "entity_type_id": OPERATOR_MAP["eq"],
        "manufacturer": OPERATOR_MAP["ilike"],
        "model": OPERATOR_MAP["ilike"],
        "status": OPERATOR_MAP["eq"],
    },
}
