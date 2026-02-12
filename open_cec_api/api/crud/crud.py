import open_cec_api.services.database.models as models
from open_cec_api.api.crud.base import CRUDClass


class CertificateCRUD(CRUDClass[models.Certificate]):
    model_type = models.Certificate


class DeviceClassAttributeCRUD(CRUDClass[models.DeviceClassAttribute]):
    model_type = models.DeviceClassAttribute


class DeviceClassCRUD(CRUDClass[models.DeviceClass]):
    model_type = models.DeviceClass


class EntityTypeCRUD(CRUDClass[models.EntityType]):
    model_type = models.EntityType


class KeyCRUD(CRUDClass[models.Key]):
    model_type = models.Key


class ListingDeviceClassAttributeCRUD(CRUDClass[models.ListingDeviceClassAttribute]):
    model_type = models.ListingDeviceClassAttribute


class ListingDeviceClassCRUD(CRUDClass[models.ListingDeviceClass]):
    model_type = models.ListingDeviceClass


class ListingCRUD(CRUDClass[models.Listing]):
    model_type = models.Listing
