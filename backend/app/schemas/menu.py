from typing import Optional, List
from datetime import datetime
from app.schemas.base import BaseSchema

class MenuBaseVO(BaseSchema):
    name: str
    permission: Optional[str] = ""
    type: int
    sort: int = 0
    parent_id: int = 0
    path: Optional[str] = ""
    icon: Optional[str] = ""
    component: Optional[str] = None
    component_name: Optional[str] = None
    status: int = 0
    visible: bool = True
    keep_alive: bool = True
    always_show: bool = True

class MenuRespVO(MenuBaseVO):
    id: int
    create_time: datetime
    children: Optional[List["MenuRespVO"]] = None

class MenuSaveReqVO(MenuBaseVO):
    id: Optional[int] = None

class MenuSimpleRespVO(BaseSchema):
    id: int
    name: str
    parent_id: int
    type: int
