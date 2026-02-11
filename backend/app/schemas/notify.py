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

# --- Notify Template Schemas ---

class NotifyTemplateBaseVO(BaseSchema):
    name: str
    code: str
    nickname: str
    content: str
    type: int
    params: Optional[List[str]] = None
    status: int
    remark: Optional[str] = None

class NotifyTemplateCreateReqVO(NotifyTemplateBaseVO):
    pass

class NotifyTemplateUpdateReqVO(NotifyTemplateBaseVO):
    id: int

class NotifyTemplateRespVO(NotifyTemplateBaseVO):
    id: int
    create_time: datetime

class NotifyTemplatePageReqVO(PageParam):
    name: Optional[str] = None
    code: Optional[str] = None
    status: Optional[int] = None
    type: Optional[int] = None
    create_time: Optional[List[datetime]] = None

class NotifySendReqVO(BaseSchema):
    user_id: int
    template_code: str
    template_params: Dict
