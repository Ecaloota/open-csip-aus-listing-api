from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from open_cec_api.api.auth import check_key_header
from open_cec_api.services.database.db import get_db_session

HeaderDependency = Depends(check_key_header)
SessionDependency = Annotated[Session, Depends(get_db_session)]

# We cannot pass the SessionDependency directly to the APIRouter
router = APIRouter(dependencies=[HeaderDependency])


# TODO remove this endpoint when the API is ready
@router.get("/")
def status_check(session: SessionDependency) -> str:
    """
    Checks the health of a project.
    """

    # TODO remove this
    print(f"Session dependency {session}")

    return "OK"
