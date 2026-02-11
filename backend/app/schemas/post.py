from typing import Optional, List
from datetime import datetime
from app.schemas.base import BaseSchema, PageParam

class PostBaseVO(BaseSchema):
    name: str
    code: str
    sort: Optional[int] = 0
    status: Optional[int] = 0
    remark: Optional[str] = None

class PostRespVO(PostBaseVO):
    id: int
    create_time: datetime

class PostSaveReqVO(PostBaseVO):
    id: Optional[int] = None

class PostPageReqVO(PageParam):
    name: Optional[str] = None
    code: Optional[str] = None
    status: Optional[int] = None

class PostSimpleRespVO(BaseSchema):
    id: int
    name: str
