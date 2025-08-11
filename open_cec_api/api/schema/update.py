"""Update models for PATCH operations"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from open_cec_api.api.schema.enums import AttributeTypeEnum, StatusEnum


# Update models (for PATCH operations)
class EntityTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None


class DeviceClassUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    requires_inverter: Optional[bool] = None


class ListingUpdate(BaseModel):
    entity_type_id: Optional[int] = None
    manufacturer: Optional[str] = Field(None, max_length=255)
    model: Optional[str] = Field(None, max_length=255)
    version: Optional[str] = Field(None, max_length=100)
    csip_aus_version: Optional[str] = Field(None, max_length=50)
    certification_body: Optional[str] = Field(None, max_length=255)
    certification_date: Optional[date] = None
    certification_expiry: Optional[date] = None
    status: Optional[StatusEnum] = None


class ListingDeviceClassUpdate(BaseModel):
    is_primary: Optional[bool] = None


class DeviceClassAttributeUpdate(BaseModel):
    attribute_name: Optional[str] = Field(None, max_length=100)
    attribute_type: Optional[AttributeTypeEnum] = None
    is_required: Optional[bool] = None
    enum_values: Optional[list[str]] = None
    description: Optional[str] = None


class ListingDeviceClassAttributeUpdate(BaseModel):
    attribute_value: Optional[str] = None


class CertificateUpdate(BaseModel):
    certificate_data: Optional[str] = None
