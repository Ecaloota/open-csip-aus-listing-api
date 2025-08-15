from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from open_cec_api.api.auth import check_key_header
from open_cec_api.api.crud import ListingCRUD
from open_cec_api.api.schema.read import ListingBase
from open_cec_api.services.database.db import get_db_session

HeaderDependency = Depends(check_key_header)
SessionDependency = Annotated[Session, Depends(get_db_session)]

# We cannot pass the SessionDependency directly to the APIRouter
public_router = APIRouter(dependencies=[HeaderDependency], tags=["Public"])

# TODO we may wish to define endpoints which allow the user to perform extended
# operations (e.g. create listings with associated cert in one step, or get
# listings with their certs in one call, etc)


@public_router.get("/")
def status_check(session: SessionDependency) -> dict[str, str]:
    """
    Checks the health of a project.
    """
    return {"API Status": "UP", "Database Status": "UP" if session else "DOWN"}


# TODO add a filter by time created or updated
@public_router.get("/listings", response_model=ListingBase | list[ListingBase])
def get_listings(
    session: SessionDependency,
    id: Optional[int] = Query(None, description="Listing ID to fetch"),
    entity_type: Optional[str] = Query(None),
    manufacturer: Optional[str] = Query(None),
    model: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    et_id = None
    if entity_type == "client":
        et_id = 1
    elif entity_type == "server":
        et_id = 2

    filters = {
        k: v
        for k, v in {
            "entity_type_id": et_id,
            "manufacturer": manufacturer,
            "model": model,
            "status": status,
        }.items()
        if v is not None
    }

    result = ListingCRUD.get(session, id=id, **filters)

    if result is None:
        raise HTTPException(status_code=404, detail="Listing not found")

    return result
