"""Base models with all fields, for reading from DB"""

from datetime import datetime

from open_cec_api.api.schema.create import (
    CertificateCreate,
    DeviceClassAttributeCreate,
    DeviceClassCreate,
    EntityTypeCreate,
    KeyCreate,
    ListingCreate,
    ListingDeviceClassAttributeCreate,
    ListingDeviceClassCreate,
)


class KeyBase(KeyCreate):
    id: int

    class Config:
        from_attributes = True


class EntityTypeBase(EntityTypeCreate):
    id: int

    class Config:
        from_attributes = True


class DeviceClassBase(DeviceClassCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ListingBase(ListingCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ListingDeviceClassBase(ListingDeviceClassCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class DeviceClassAttributeBase(DeviceClassAttributeCreate):
    id: int

    class Config:
        from_attributes = True


class ListingDeviceClassAttributeBase(ListingDeviceClassAttributeCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CertificateBase(CertificateCreate):
    id: int

    class Config:
        from_attributes = True
