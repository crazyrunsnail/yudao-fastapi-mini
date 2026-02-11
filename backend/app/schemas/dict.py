from typing import Optional, List
from datetime import datetime
from app.schemas.base import BaseSchema, PageParam

# --- Dict Type ---

class DictTypeBaseVO(BaseSchema):
    name: str
    type: str
    status: Optional[int] = 0
    remark: Optional[str] = None

class DictTypeRespVO(DictTypeBaseVO):
    id: int
    create_time: datetime

class DictTypePageReqVO(PageParam):
    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[int] = None
    create_time: Optional[List[datetime]] = None

class DictTypeSaveReqVO(DictTypeBaseVO):
    id: Optional[int] = None

class DictTypeSimpleRespVO(BaseSchema):
    id: int
    name: str
    type: str

# --- Dict Data ---

class DictDataBaseVO(BaseSchema):
    sort: int
    label: str
    value: str
    dict_type: str
    status: Optional[int] = 0
    color_type: Optional[str] = ""
    css_class: Optional[str] = ""
    remark: Optional[str] = None

class DictDataRespVO(DictDataBaseVO):
    id: int
    create_time: datetime

class DictDataPageReqVO(PageParam):
    label: Optional[str] = None
    dict_type: Optional[str] = None
    status: Optional[int] = None

class DictDataSaveReqVO(DictDataBaseVO):
    id: Optional[int] = None

class DictDataSimpleRespVO(BaseSchema):
    dict_type: str
    label: str
    value: str
    color_type: Optional[str] = ""
    css_class: Optional[str] = ""
