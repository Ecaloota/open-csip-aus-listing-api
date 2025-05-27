from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from passlib.context import CryptContext

from open_cec_api.settings import settings

"""Basic API key authentication; does not identify particular users"""

pwd_context = CryptContext(schemes=["des_crypt"], deprecated="auto")
api_key_header = APIKeyHeader(name="x-api-key")


def verify_key(plain_key: str, hash: str) -> bool:
    return pwd_context.verify(plain_key, hash)


def get_key_hash(key: str) -> str:
    return pwd_context.hash(key)


def check_key_header(api_key: str = Security(api_key_header)) -> None:
    """
    If the provided api_key is valid (matches the build secret), continue.
    Otherwise, raise a HTTPException 401.
    """

    if not verify_key(api_key, settings.api_key_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key header, or invalid API key",
        )
