from typing import Optional, List
from datetime import datetime
from app.schemas.base import BaseSchema
from app.common.paging import PageParam

class RoleBaseVO(BaseSchema):
    name: str
    code: str
    sort: int
    status: Optional[int] = 0
    type: Optional[int] = 2 # 默认自定义角色
    remark: Optional[str] = None

class RolePageReqVO(PageParam, BaseSchema):
    name: Optional[str] = None
    code: Optional[str] = None
    status: Optional[int] = None
    create_time: Optional[List[datetime]] = None

class RoleRespVO(RoleBaseVO):
    id: int
    data_scope: int
    data_scope_dept_ids: Optional[str] = ""
    create_time: datetime

class RoleSaveReqVO(RoleBaseVO):
    id: Optional[int] = None

class RoleUpdateStatusReqVO(BaseSchema):
    id: int
    status: int
