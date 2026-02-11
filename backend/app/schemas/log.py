from typing import Optional, List
from datetime import datetime
from app.schemas.base import BaseSchema, PageParam

# --- Login Log ---

class LoginLogRespVO(BaseSchema):
    id: int
    log_type: int
    trace_id: str
    username: str
    user_ip: str
    user_agent: str
    result: int
    user_id: Optional[int]
    user_type: int
    create_time: datetime

class LoginLogPageReqVO(PageParam):
    username: Optional[str] = None
    user_ip: Optional[str] = None
    result: Optional[int] = None
    create_time: Optional[List[str]] = None

# --- Operate Log ---

class OperateLogRespVO(BaseSchema):
    id: int
    trace_id: str
    user_id: int
    user_name: Optional[str] = None
    user_type: int
    type: str
    sub_type: str
    biz_id: int
    action: str
    success: bool
    extra: str
    request_method: str
    request_url: str
    user_ip: str
    user_agent: str
    create_time: datetime

class OperateLogPageReqVO(PageParam):
    type: Optional[str] = None
    user_id: Optional[int] = None
    success: Optional[bool] = None
    create_time: Optional[List[str]] = None

