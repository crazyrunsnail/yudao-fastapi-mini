from fastapi import APIRouter, Depends, Query, Body, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.permission import PermissionAssignRoleMenuReqVO, PermissionAssignUserRoleReqVO
from app.services.permission_service import PermissionService
from app.common.response import CommonResult
from typing import Set, List
from app.core.auth import get_login_user
from app.common.operate_log import operate_log

router = APIRouter(prefix="/system/permission", tags=["管理后台 - 权限分配"])

@router.get("/list-role-menus", response_model=CommonResult[Set[int]])
async def list_role_menus(role_id: int = Query(...), db: AsyncSession = Depends(get_db)):
    result = await PermissionService.get_role_menu_ids(db, role_id)
    return CommonResult.success(data=result)

@router.post("/assign-role-menu", response_model=CommonResult[bool])
@operate_log(type="权限分配", sub_type="分配角色菜单", biz_id_field="role_id")
async def assign_role_menu(request: Request, req: PermissionAssignRoleMenuReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    await PermissionService.assign_role_menu(db, req.role_id, req.menu_ids)
    return CommonResult.success(data=True)

@router.get("/list-user-roles", response_model=CommonResult[Set[int]])
async def list_user_roles(user_id: int = Query(...), db: AsyncSession = Depends(get_db)):
    result = await PermissionService.get_user_role_ids(db, user_id)
    return CommonResult.success(data=result)

@router.post("/assign-user-role", response_model=CommonResult[bool])
@operate_log(type="权限分配", sub_type="分配用户角色", biz_id_field="user_id")
async def assign_user_role(request: Request, req: PermissionAssignUserRoleReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    await PermissionService.assign_user_role(db, req.user_id, req.role_ids)
    return CommonResult.success(data=True)
