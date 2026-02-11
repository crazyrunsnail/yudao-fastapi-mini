from typing import Optional, List
from datetime import datetime
from app.schemas.base import BaseSchema, PageParam

class TenantPackageBaseVO(BaseSchema):
    name: str
    status: Optional[int] = None
    menu_ids: Optional[List[int]] = [] # 前端传数组，后端存逗号分隔字符串
    remark: Optional[str] = None

class TenantPackagePageReqVO(PageParam, BaseSchema):
    name: Optional[str] = None
    status: Optional[int] = None
    create_time: Optional[List[datetime]] = None

class TenantPackageRespVO(BaseSchema):
    id: int
    name: str
    status: int
    menu_ids: List[int]
    remark: Optional[str] = None
    create_time: datetime

class TenantPackageSimpleRespVO(BaseSchema):
    id: int
    name: str

class TenantPackageSaveReqVO(TenantPackageBaseVO):
    id: Optional[int] = None
