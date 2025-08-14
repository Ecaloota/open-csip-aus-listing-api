"""Base models for creation"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from open_cec_api.api.schema.enums import AttributeTypeEnum, StatusEnum


class EntityTypeCreate(BaseModel):
    name: str = Field(
        ..., max_length=50, description="Entity type name (server, client)"
    )
    description: Optional[str] = None


class DeviceClassCreate(BaseModel):
    name: str = Field(
        ..., max_length=100, description="Device class name (BESS, inverter, etc.)"
    )
    description: Optional[str] = None


class ListingCreate(BaseModel):
    entity_type_id: int
    manufacturer: str = Field(..., max_length=255)
    model: str = Field(..., max_length=255)
    status: StatusEnum = StatusEnum.active


class ListingDeviceClassCreate(BaseModel):
    listing_id: int
    device_class_id: int


class DeviceClassAttributeCreate(BaseModel):
    device_class_id: int
    attribute_name: str = Field(..., max_length=100)
    attribute_type: AttributeTypeEnum
    description: Optional[str] = None


class ListingDeviceClassAttributeCreate(BaseModel):
    listing_id: int
    device_class_id: int
    attribute_name: str = Field(..., max_length=100)
    attribute_value: Optional[str] = None


class CertificateCreate(BaseModel):
    listing_id: int
    expiry: date
    certification_date: date
    certifying_body: str = Field(..., max_length=100)
    test_profiles: Optional[list[str]] = None
