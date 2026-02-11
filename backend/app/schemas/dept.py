from typing import Optional, List
from datetime import datetime
from app.schemas.base import BaseSchema, PageParam

class DeptBaseVO(BaseSchema):
    name: str
    parent_id: Optional[int] = 0
    sort: Optional[int] = 0
    leader_user_id: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    status: Optional[int] = 0

class DeptRespVO(DeptBaseVO):
    id: int
    create_time: datetime

class DeptSaveReqVO(DeptBaseVO):
    id: Optional[int] = None

class DeptListReqVO(BaseSchema):
    name: Optional[str] = None
    status: Optional[int] = None

class DeptSimpleRespVO(BaseSchema):
    id: int
    name: str
    parent_id: int
