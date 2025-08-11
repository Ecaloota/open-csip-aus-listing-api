"""Base models for creation"""

from datetime import date
from typing import List, Optional

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
    requires_inverter: bool = False


class ListingCreate(BaseModel):
    entity_type_id: int
    manufacturer: str = Field(..., max_length=255)
    model: str = Field(..., max_length=255)
    version: Optional[str] = Field(None, max_length=100)
    csip_aus_version: str = Field(..., max_length=50)
    certification_body: Optional[str] = Field(None, max_length=255)
    certification_date: Optional[date] = None
    certification_expiry: Optional[date] = None
    status: StatusEnum = StatusEnum.active


class ListingDeviceClassCreate(BaseModel):
    listing_id: int
    device_class_id: int
    is_primary: bool = False


class DeviceClassAttributeCreate(BaseModel):
    device_class_id: int
    attribute_name: str = Field(..., max_length=100)
    attribute_type: AttributeTypeEnum
    is_required: bool = False
    enum_values: Optional[List[str]] = None
    description: Optional[str] = None


class ListingDeviceClassAttributeCreate(BaseModel):
    listing_id: int
    device_class_id: int
    attribute_name: str = Field(..., max_length=100)
    attribute_value: Optional[str] = None


class CertificateCreate(BaseModel):
    listing_id: int
    certificate_data: Optional[str] = None
