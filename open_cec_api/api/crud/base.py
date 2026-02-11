from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar, Union

from sqlalchemy.orm import Session

from open_cec_api.services.database.models import Base as ModelBase

T = TypeVar("T", bound=ModelBase)


class CRUDClass(ABC, Generic[T]):
    @staticmethod
    @abstractmethod
    def get(session: Session, *args, **kwargs) -> Union[T, list[T], None]: ...

    @staticmethod
    @abstractmethod
    def create(session: Session, *args, **kwargs) -> ModelBase: ...

    @staticmethod
    @abstractmethod
    def update(session: Session, *args, **kwargs) -> Optional[ModelBase]: ...

    @staticmethod
    @abstractmethod
    def delete(session: Session, id: int) -> bool: ...
