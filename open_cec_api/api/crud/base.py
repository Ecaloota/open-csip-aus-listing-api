from abc import ABC
from typing import Generic, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy.orm import Session

from open_cec_api.api.crud.filters import CLS_TO_KW_FILTERS
from open_cec_api.services.database.models import Base as ModelBase

T = TypeVar("T", bound=ModelBase)


class CRUDClass(ABC, Generic[T]):
    model_type: Type[T]  # subclasses must set this

    @classmethod
    def get(
        cls, session: Session, id: int | None = None, *args, **kwargs
    ) -> Union[T, list[T], None]:
        query = session.query(cls.model_type)

        if id is not None:
            return query.filter(getattr(cls.model_type, "id") == id).first()

        # apply filters
        cls_filter = CLS_TO_KW_FILTERS[cls.model_type]
        for k, v in kwargs.items():
            filter = cls_filter.get(k, None)
            if not filter:
                raise ValueError

            expression = filter(getattr(cls.model_type, k), v)
            query = query.filter(expression)

        return query.all()

    @classmethod
    def create(cls, session: Session, schema: BaseModel, *args, **kwargs) -> T:
        instance = cls.model_type(**schema.model_dump())
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance

    @classmethod
    def update(
        cls, session: Session, id: int, schema: BaseModel, *args, **kwargs
    ) -> Optional[T]:
        instance = session.query(cls.model_type).filter(cls.model_type.id == id).first()
        if instance:
            update_data = schema.model_dump(exclude_unset=True)
            for f, v in update_data.items():
                if hasattr(instance, f):
                    setattr(instance, f, v)
            session.commit()
            session.refresh(instance)
        return instance

    @classmethod
    def delete(cls, session: Session, id: int) -> bool:
        instance = session.query(cls.model_type).filter(cls.model_type.id == id).first()
        if instance:
            session.delete(instance)
            session.commit()
            return True
        return False
