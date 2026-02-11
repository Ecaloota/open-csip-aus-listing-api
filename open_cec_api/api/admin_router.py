from typing import Annotated, Optional, TypeVar, Union

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

import open_cec_api.api.crud as crud
import open_cec_api.api.schema.create as create_schema
import open_cec_api.api.schema.read as read_schema
import open_cec_api.api.schema.update as update_schema
from open_cec_api.api.auth import check_key_header
from open_cec_api.api.crud.base import CRUDClass
from open_cec_api.services.database.db import get_db_session
from open_cec_api.services.database.models import Base as ModelBase

HeaderDependency = Depends(check_key_header)
SessionDependency = Annotated[Session, Depends(get_db_session)]

# We cannot pass the SessionDependency directly to the APIRouter
admin_router = APIRouter(dependencies=[HeaderDependency], tags=["Admin"])

# TODO we may wish to define endpoints which allow the user to perform extended
# operations (e.g. create listings with associated cert in one step, or get
# listings with their certs in one call, etc)

# TODO some of these have a bug maybe wherein only the first in a list is returned?
# e.g. for example element 7 (BESS + inverter), we only get one attribute not the list
# of expected attributes. I suspect this is an issue with the CRUD get method?
# but just looked and couldn't see the issue

T = TypeVar("T", bound=ModelBase)


def register_crud_routes(
    router: APIRouter,
    path: str,
    crud_class: type[CRUDClass[T]],
    base_schema: type[BaseModel],
    _create_schema: type[BaseModel],
    _update_schema: type[BaseModel],
    filter_fields: list[str],
):
    """Register GET, POST, PUT, DELETE routes for a model."""

    # Dynamically build the function signature for GET
    from inspect import Parameter, Signature

    # Prepare parameters: id + filter fields + db
    params = [
        Parameter(
            "id",
            kind=Parameter.POSITIONAL_OR_KEYWORD,
            default=None,
            annotation=Optional[int],
        )
    ]
    for f in filter_fields:
        params.append(
            Parameter(
                f,
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Query(None),
                annotation=Optional[str],
            )
        )
    params.append(
        Parameter(
            "session",
            kind=Parameter.POSITIONAL_OR_KEYWORD,
            default=None,
            annotation=SessionDependency,
        )
    )

    async def get_items(
        session: SessionDependency, id: Optional[int] = Query(None), **filters
    ):
        filters = {k: v for k, v in filters.items() if v is not None}
        result = crud_class.get(session, id=id, **filters)
        if id is not None and result is None:
            raise HTTPException(
                status_code=404, detail=f"{base_schema.__name__} not found"
            )
        return result

    get_items.__signature__ = Signature(parameters=params)

    router.get(
        path,
        response_model=Union[base_schema, list[base_schema]],
        summary=f"Get {base_schema.__name__}(s)",
    )(get_items)

    async def create_item(
        session: SessionDependency,
        item_data: _create_schema,  # type: ignore
    ):
        try:
            return crud_class.create(session, item_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    router.post(
        path, response_model=base_schema, summary=f"Create {base_schema.__name__}"
    )(create_item)

    async def update_item(
        id: int,
        item_data: _update_schema,  # type: ignore
        session: SessionDependency,
    ):
        result = crud_class.update(session, id, item_data)
        if result is None:
            raise HTTPException(
                status_code=404, detail=f"{base_schema.__name__} not found"
            )
        return result

    router.put(
        f"{path}/{{id}}",
        response_model=base_schema,
        summary=f"Update {base_schema.__name__}",
    )(update_item)

    async def delete_item(id: int, session: SessionDependency):
        result = crud_class.delete(session, id)
        if not result:
            raise HTTPException(
                status_code=404, detail=f"{base_schema.__name__} not found"
            )
        return result

    router.delete(
        f"{path}/{{id}}",
        response_model=base_schema,
        summary=f"Delete {base_schema.__name__}",
        status_code=status.HTTP_200_OK,
    )(delete_item)


# Keys
register_crud_routes(
    admin_router,
    "/admin/keys",
    crud.KeyCRUD,
    read_schema.KeyBase,
    create_schema.KeyCreate,
    update_schema.KeyUpdate,
    ["value", "description"],
)

# Entity Types
register_crud_routes(
    admin_router,
    "/admin/entity-types",
    crud.EntityTypeCRUD,
    read_schema.EntityTypeBase,
    create_schema.EntityTypeCreate,
    update_schema.EntityTypeUpdate,
    ["name"],
)

# Device Classes
register_crud_routes(
    admin_router,
    "/admin/device-classes",
    crud.DeviceClassCRUD,
    read_schema.DeviceClassBase,
    create_schema.DeviceClassCreate,
    update_schema.DeviceClassUpdate,
    ["name"],
)

# Listings
register_crud_routes(
    admin_router,
    "/admin/listings",
    crud.ListingCRUD,
    read_schema.ListingBase,
    create_schema.ListingCreate,
    update_schema.ListingUpdate,
    ["entity_type_id", "manufacturer", "model", "status"],
)

# Listing Device Classes
register_crud_routes(
    admin_router,
    "/admin/listing-device-classes",
    crud.ListingDeviceClassCRUD,
    read_schema.ListingDeviceClassBase,
    create_schema.ListingDeviceClassCreate,
    update_schema.ListingDeviceClassUpdate,
    ["listing_id", "device_class_id"],
)

# Device Class Attributes
register_crud_routes(
    admin_router,
    "/admin/device-class-attributes",
    crud.DeviceClassAttributeCRUD,
    read_schema.DeviceClassAttributeBase,
    create_schema.DeviceClassAttributeCreate,
    update_schema.DeviceClassAttributeUpdate,
    ["device_class_id", "attribute_name"],
)

# Listing Device Class Attributes
register_crud_routes(
    admin_router,
    "/admin/listing-device-class-attributes",
    crud.ListingDeviceClassAttributeCRUD,
    read_schema.ListingDeviceClassAttributeBase,
    create_schema.ListingDeviceClassAttributeCreate,
    update_schema.ListingDeviceClassAttributeUpdate,
    ["listing_id", "device_class_id", "attribute_name"],
)

# Certificates
register_crud_routes(
    admin_router,
    "/admin/certificates",
    crud.CertificateCRUD,
    read_schema.CertificateBase,
    create_schema.CertificateCreate,
    update_schema.CertificateUpdate,
    ["listing_id", "certifying_body"],
)


@admin_router.get("/foo")
async def foo(session: SessionDependency, id: Optional[int] = None):
    from open_cec_api.api.crud.extended import get

    return get(session, id)
