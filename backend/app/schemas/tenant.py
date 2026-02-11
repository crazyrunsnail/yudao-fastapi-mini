from typing import Optional, List
from datetime import datetime
from app.schemas.base import BaseSchema, PageParam

class TenantBaseVO(BaseSchema):
    name: str
    contact_name: Optional[str] = None
    contact_mobile: Optional[str] = None
    status: Optional[int] = None
    websites: Optional[str] = None
    package_id: Optional[int] = None
    expire_time: Optional[datetime] = None
    account_count: Optional[int] = None

class TenantPageReqVO(PageParam, BaseSchema):
    name: Optional[str] = None
    contact_name: Optional[str] = None
    status: Optional[int] = None
    create_time: Optional[List[datetime]] = None

class TenantRespVO(BaseSchema):
    id: int
    name: str
    contact_name: Optional[str] = None
    contact_mobile: Optional[str] = None
    status: Optional[int] = None
    websites: Optional[str] = None
    package_id: Optional[int] = None
    expire_time: Optional[datetime] = None
    account_count: Optional[int] = None
    create_time: datetime

class TenantSaveReqVO(TenantBaseVO):
    id: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
