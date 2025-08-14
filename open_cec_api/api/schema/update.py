"""Update models for PATCH operations"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from open_cec_api.api.schema.enums import AttributeTypeEnum, StatusEnum


# Update models (for PATCH operations)
class KeyUpdate(BaseModel):
    value: Optional[str] = Field(default=None, max_length=50)
    description: Optional[str] = None


class EntityTypeUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=50)
    description: Optional[str] = None


class DeviceClassUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None


class ListingUpdate(BaseModel):
    entity_type_id: Optional[int] = None
    manufacturer: Optional[str] = Field(default=None, max_length=255)
    model: Optional[str] = Field(default=None, max_length=255)
    status: Optional[StatusEnum] = None


class DeviceClassAttributeUpdate(BaseModel):
    attribute_name: Optional[str] = Field(default=None, max_length=100)
    attribute_type: Optional[AttributeTypeEnum] = None
    description: Optional[str] = None


class ListingDeviceClassAttributeUpdate(BaseModel):
    attribute_value: Optional[str] = None


class CertificateUpdate(BaseModel):
    expiry: Optional[date] = None
    certification_date: Optional[date] = None
    certifying_body: Optional[str] = Field(default=None, max_length=100)
    test_profiles: Optional[list[str]] = None
