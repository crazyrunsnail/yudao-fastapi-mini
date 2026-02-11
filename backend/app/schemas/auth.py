from typing import Optional, List
from datetime import datetime
from app.schemas.base import BaseSchema
from app.schemas.menu import MenuRespVO

class AuthLoginReqVO(BaseSchema):
    username: str
    password: str
    captcha_verification: Optional[str] = None

class AuthLoginRespVO(BaseSchema):
    user_id: int
    access_token: str
    refresh_token: str
    expires_time: datetime

class AuthSmsLoginReqVO(BaseSchema):
    mobile: str
    code: str

# 获取权限信息的响应对象
class UserInfoVO(BaseSchema):
    id: int
    nickname: str
    avatar: Optional[str] = ""
    username: str

class AuthPermissionInfoRespVO(BaseSchema):
    user: UserInfoVO
    roles: List[str]
    permissions: List[str]
    menus: List[MenuRespVO]
