from typing import Optional, List, Dict
from datetime import datetime, date
from app.schemas.base import BaseSchema, PageParam

class NotifyMessageBaseVO(BaseSchema):
    user_id: int
    user_type: int
    template_id: int
    template_code: str
    template_nickname: str
    template_content: str
    template_type: int
    template_params: Dict
    read_status: bool
    read_time: Optional[datetime] = None

class NotifyMessageRespVO(NotifyMessageBaseVO):
    id: int
    create_time: datetime

class NotifyMessagePageReqVO(PageParam):
    user_id: Optional[int] = None
    user_type: Optional[int] = None
    template_code: Optional[str] = None
    template_type: Optional[int] = None
    create_time: Optional[List[datetime]] = None

class NotifyMessageMyPageReqVO(PageParam):
    read_status: Optional[bool] = None
    create_time: Optional[List[datetime]] = None
