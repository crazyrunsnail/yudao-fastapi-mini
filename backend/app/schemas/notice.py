from typing import Optional, List
from datetime import datetime
from app.schemas.base import BaseSchema, PageParam

class NoticeBaseVO(BaseSchema):
    title: str
    type: int
    content: str
    status: Optional[int] = 0
    remark: Optional[str] = None

class NoticeCreateReqVO(NoticeBaseVO):
    pass

class NoticeUpdateReqVO(NoticeBaseVO):
    id: int

class NoticeRespVO(NoticeBaseVO):
    id: int
    create_time: datetime

class NoticePageReqVO(PageParam):
    title: Optional[str] = None
    status: Optional[int] = None
