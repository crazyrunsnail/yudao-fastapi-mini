from fastapi import Depends, Header, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.token_service import TokenService
from app.models.user import SystemUser
from sqlalchemy import select
from typing import List, Set, Optional

security = HTTPBearer()

async def get_login_user(
    auth: HTTPAuthorizationCredentials = Security(security),
    db: AsyncSession = Depends(get_db)
) -> SystemUser:
    token = auth.credentials
    token_data = await TokenService.get_access_token(db, token)
    if not token_data:
        raise HTTPException(status_code=401, detail="登录已过期或无效")
    
    user_id = token_data.get("userId")
    # 这里可以考虑加缓存
    result = await db.execute(select(SystemUser).where(SystemUser.id == user_id, SystemUser.deleted == 0))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    if user.status != 0:
        raise HTTPException(status_code=401, detail="用户已被禁用")
    
    return user

class PermissionChecker:
    def __init__(self, permission: str):
        self.permission = permission

    async def __call__(
        self,
        current_user: SystemUser = Depends(get_login_user),
        db: AsyncSession = Depends(get_db)
    ):
        # 1. 如果是超级管理员，直接放行
        # 这里硬编码判断 ID 为 1 或者角色包含 super_admin
        # 实际开发中建议查询角色表
        from app.services.permission_service import PermissionService
        from app.services.role_service import RoleService
        
        role_ids = await PermissionService.get_user_role_ids(db, current_user.id)
        if not role_ids:
            if not self.permission: return # 只要登录就行
            raise HTTPException(status_code=403, detail="没有权限")
            
        roles = []
        for rid in role_ids:
            role = await RoleService.get_role(db, rid)
            if role and role.status == 0:
                roles.append(role)
        
        # 检查是否是超级管理员
        is_super = any(role.code == "super_admin" for role in roles)
        if is_super:
            return True
            
        if not self.permission:
            return True

        # 2. 获取用户的所有菜单权限
        user_permissions = await PermissionService.get_user_permissions(db, current_user.id)
        if self.permission not in user_permissions:
            raise HTTPException(status_code=403, detail=f"没有权限: {self.permission}")
            
        return True

def has_permission(permission: str):
    return Depends(PermissionChecker(permission))
