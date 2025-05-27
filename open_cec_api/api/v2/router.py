from fastapi import APIRouter, Depends

from open_cec_api.api.auth import check_key_header

# TODO add database session dependency
router = APIRouter(dependencies=[Depends(check_key_header)])


# TODO remove this endpoint when the API is ready
@router.get("/foo")
def status_check_v2() -> str:
    """
    Checks the health of a project.
    """

    return "NOT OK"
