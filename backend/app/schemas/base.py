from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )

from typing import Generic, TypeVar, List
T = TypeVar("T")

class PageParam(BaseSchema):
    page_no: int = 1
    page_size: int = 10

class PageResult(BaseSchema, Generic[T]):
    list: List[T]
    total: int
