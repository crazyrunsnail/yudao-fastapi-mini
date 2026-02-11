from typing import Optional, List
from datetime import datetime
from app.schemas.base import BaseSchema
from app.common.paging import PageParam

class UserBaseVO(BaseSchema):
    username: str
    nickname: str
    remark: Optional[str] = None
    dept_id: Optional[int] = None
    post_ids: Optional[List[int]] = [] # 前端传数组，后端存字符串
    email: Optional[str] = None
    mobile: Optional[str] = None
    sex: Optional[int] = None
    avatar: Optional[str] = None
    status: Optional[int] = None

class UserPageReqVO(PageParam, BaseSchema):
    username: Optional[str] = None
    mobile: Optional[str] = None
    status: Optional[int] = None
    dept_id: Optional[int] = None
    create_time: Optional[List[datetime]] = None

class UserRespVO(BaseSchema):
    id: int
    username: str
    nickname: str
    remark: Optional[str] = None
    dept_id: Optional[int] = None
    dept_name: Optional[str] = None
    post_ids: Optional[List[int]] = []
    email: Optional[str] = None
    mobile: Optional[str] = None
    sex: Optional[int] = None
    avatar: Optional[str] = None
    status: Optional[int] = None
    login_ip: Optional[str] = None
    login_date: Optional[datetime] = None
    create_time: datetime

class UserSaveReqVO(UserBaseVO):
    id: Optional[int] = None
    password: Optional[str] = None

class UserUpdatePasswordReqVO(BaseSchema):
    id: int
    password: str

class UserUpdateStatusReqVO(BaseSchema):
    id: int
    status: int

class UserSimpleRespVO(BaseSchema):
    id: int
    nickname: str

class UserProfileRespVO(UserRespVO):
    roles: Optional[List[dict]] = []
    posts: Optional[List[dict]] = []
    dept: Optional[dict] = None

class UserProfileUpdateReqVO(BaseSchema):
    nickname: str
    email: Optional[str] = None
    mobile: Optional[str] = None
    sex: Optional[int] = None

class UserProfileUpdatePasswordReqVO(BaseSchema):
    old_password: str
    new_password: str

class UserImportExcelVO(BaseSchema):
    username: str
    nickname: str
    dept_id: Optional[int] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    sex: Optional[int] = None
    status: Optional[int] = None

class UserImportRespVO(BaseSchema):
    create_usernames: List[str]
    update_usernames: List[str]
    failure_usernames: Dict[str, str]
