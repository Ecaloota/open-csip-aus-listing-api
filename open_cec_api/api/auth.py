from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from open_cec_api.services.database.db import get_db_session
from open_cec_api.services.database.models import Key

"""Basic API key authentication; does not identify particular users"""

pwd_context = CryptContext(schemes=["des_crypt"], deprecated="auto")
api_key_header = APIKeyHeader(name="x-api-key")


def verify_key(plain_key: str, hash: str) -> bool:
    return pwd_context.verify(plain_key, hash)


def get_key_hash(key: str) -> str:
    return pwd_context.hash(key)


def check_key_header(
    session: Annotated[Session, Depends(get_db_session)],
    key: str = Security(api_key_header),
):
    if not key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="API key required"
        )

    # not very efficient but ok with number of keys required
    with session:
        k_records = session.query(Key).all()

    for k in k_records:
        if verify_key(key, k.value):  # type: ignore
            return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key"
    )
