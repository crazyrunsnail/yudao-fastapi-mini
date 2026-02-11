from fastapi import APIRouter, Depends, Query, Body, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.role import RolePageReqVO, RoleRespVO, RoleSaveReqVO, RoleUpdateStatusReqVO
from app.services.role_service import RoleService
from app.common.response import CommonResult
from app.common.paging import PageResult
from app.schemas.base import BaseSchema
from typing import List
from app.core.auth import get_login_user, has_permission
from app.common.operate_log import operate_log

router = APIRouter(prefix="/system/role", tags=["管理后台 - 角色"])

class RoleSimpleRespVO(BaseSchema):
    id: int
    name: str

@router.get("/page", response_model=CommonResult[PageResult[RoleRespVO]])
@operate_log(type="角色管理", sub_type="查询角色分页")
async def get_role_page(request: Request, req: RolePageReqVO = Depends(), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    result = await RoleService.get_role_page(db, req)
    return CommonResult.success(data=result)

@router.get("/get", response_model=CommonResult[RoleRespVO])
@operate_log(type="角色管理", sub_type="查看角色详情", biz_id_field="id")
async def get_role(request: Request, id: int = Query(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    role = await RoleService.get_role(db, id)
    return CommonResult.success(data=role)

@router.post("/create", response_model=CommonResult[int])
@operate_log(type="角色管理", sub_type="新增角色")
async def create_role(request: Request, req: RoleSaveReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    role_id = await RoleService.create_role(db, req)
    return CommonResult.success(data=role_id)

@router.put("/update", response_model=CommonResult[bool])
@operate_log(type="角色管理", sub_type="修改角色")
async def update_role(request: Request, req: RoleSaveReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    await RoleService.update_role(db, req)
    return CommonResult.success(data=True)

@router.delete("/delete", response_model=CommonResult[bool])
@operate_log(type="角色管理", sub_type="删除角色", biz_id_field="id")
async def delete_role(request: Request, id: int = Query(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    await RoleService.delete_role(db, id)
    return CommonResult.success(data=True)

@router.put("/update-status", response_model=CommonResult[bool])
@operate_log(type="角色管理", sub_type="修改角色状态")
async def update_role_status(request: Request, req: RoleUpdateStatusReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    # 简单的状态更新逻辑
    from sqlalchemy import select
    from app.models.role import SystemRole
    stmt = select(SystemRole).where(SystemRole.id == req.id)
    target_role = (await db.execute(stmt)).scalar_one_or_none()
    if target_role:
        target_role.status = req.status
        await db.commit()
    return CommonResult.success(data=True)

@router.get("/simple-list", response_model=CommonResult[List[RoleSimpleRespVO]])
async def get_role_simple_list(db: AsyncSession = Depends(get_db)):
    roles = await RoleService.get_role_list_by_status(db, 0)
    return CommonResult.success(data=roles)

@router.get("/export-excel", dependencies=[has_permission("system:role:export")])
@operate_log(type="角色管理", sub_type="导出角色")
async def export_role(req: RolePageReqVO = Depends(), db: AsyncSession = Depends(get_db)):
    content = await RoleService.export_roles(db, req)
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=role_export.xlsx"}
    )
