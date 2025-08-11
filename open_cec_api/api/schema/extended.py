# # Extended models with relationships
# class DeviceClassWithAttributes(DeviceClassBase):
#     device_class_attributes: List[DeviceClassAttributeBase] = []


# class ListingDeviceClassWithDetails(ListingDeviceClassBase):
#     device_class: DeviceClassBase


# class ListingWithRelations(ListingBase):
#     entity_type: EntityTypeBase
#     listing_device_classes: List[ListingDeviceClassWithDetails] = []
#     certificates: List[CertificateBase] = []


# class ListingWithAttributes(ListingWithRelations):
#     listing_device_class_attributes: List[ListingDeviceClassAttributeBase] = []

# Specialized response models for common API operations
# class ListingSummary(BaseModel):
#     """Lightweight listing model for list views"""

#     id: int
#     manufacturer: str
#     model: str
#     version: Optional[str]
#     csip_aus_version: str
#     status: StatusEnum
#     device_classes: List[str] = []  # Just the names
#     certification_expiry: Optional[date]

#     class Config:
#         from_attributes = True


# class DeviceClassSummary(BaseModel):
#     """Lightweight device class model"""

#     id: int
#     name: str
#     description: Optional[str]
#     requires_inverter: bool

#     class Config:
#         from_attributes = True


# # Request models for complex operations
# class CreateListingWithClasses(BaseModel):
#     """Create a listing with device classes in one operation"""

#     listing: ListingCreate
#     device_class_ids: List[int]
#     primary_device_class_id: Optional[int] = None


# class AddAttributesToListing(BaseModel):
#     """Add multiple attributes to a listing"""

#     listing_id: int
#     attributes: List[ListingDeviceClassAttributeCreate]


# # Response models for bulk operations
# class BulkListingResponse(BaseModel):
#     """Response for bulk listing operations"""

#     total: int
#     items: List[ListingSummary]
#     filters_applied: dict = {}


# class ValidationError(BaseModel):
#     """Error model for validation failures"""

#     field: str
#     message: str
#     value: Optional[str] = None
