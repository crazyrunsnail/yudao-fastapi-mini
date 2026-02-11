from typing import List, Set
from app.schemas.base import BaseSchema

class PermissionAssignRoleMenuReqVO(BaseSchema):
    role_id: int
    menu_ids: Set[int]

class PermissionAssignUserRoleReqVO(BaseSchema):
    user_id: int
    role_ids: Set[int]
