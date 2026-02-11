from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import UserPageReqVO, UserRespVO, UserSaveReqVO, UserUpdateStatusReqVO, UserUpdatePasswordReqVO, UserImportRespVO
from app.services.user_service import UserService
from app.common.response import CommonResult
from app.common.paging import PageResult
from typing import List

from app.core.auth import has_permission, get_login_user
from app.common.operate_log import operate_log
from fastapi import Request, UploadFile, File
from fastapi.responses import Response

router = APIRouter(prefix="/system/user", tags=["管理后台 - 用户"])

@router.get("/page", response_model=CommonResult[PageResult[UserRespVO]], dependencies=[has_permission("system:user:query")])
@operate_log(type="用户管理", sub_type="查询用户分页")
async def get_user_page(request: Request, req: UserPageReqVO = Depends(), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    result = await UserService.get_user_page(db, req)
    return CommonResult.success(data=result)

@router.get("/get", response_model=CommonResult[UserRespVO], dependencies=[has_permission("system:user:query")])
@operate_log(type="用户管理", sub_type="查看用户详情", biz_id_field="id")
async def get_user(request: Request, id: int = Query(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    user = await UserService.get_user(db, id)
    return CommonResult.success(data=user)

@router.post("/create", response_model=CommonResult[int], dependencies=[has_permission("system:user:create")])
@operate_log(type="用户管理", sub_type="新增用户")
async def create_user(request: Request, req: UserSaveReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    user_id = await UserService.create_user(db, req)
    return CommonResult.success(data=user_id)

@router.put("/update", response_model=CommonResult[bool], dependencies=[has_permission("system:user:update")])
@operate_log(type="用户管理", sub_type="修改用户")
async def update_user(request: Request, req: UserSaveReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    await UserService.update_user(db, req)
    return CommonResult.success(data=True)

@router.delete("/delete", response_model=CommonResult[bool], dependencies=[has_permission("system:user:delete")])
@operate_log(type="用户管理", sub_type="删除用户", biz_id_field="id")
async def delete_user(request: Request, id: int = Query(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    await UserService.delete_user(db, id)
    return CommonResult.success(data=True)

@router.put("/update-password", response_model=CommonResult[bool], dependencies=[has_permission("system:user:update-password")])
@operate_log(type="用户管理", sub_type="重置用户密码")
async def update_user_password(request: Request, req: UserUpdatePasswordReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    await UserService.update_user_password(db, req.id, req.password)
    return CommonResult.success(data=True)

@router.put("/update-status", response_model=CommonResult[bool], dependencies=[has_permission("system:user:update")])
@operate_log(type="用户管理", sub_type="修改用户状态")
async def update_user_status(request: Request, req: UserUpdateStatusReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    # 简单的状态更新逻辑
    from sqlalchemy import select
    from app.models.user import SystemUser
    stmt = select(SystemUser).where(SystemUser.id == req.id)
    target_user = (await db.execute(stmt)).scalar_one_or_none()
    if target_user:
        target_user.status = req.status
        await db.commit()
    return CommonResult.success(data=True)

from app.core.auth import get_login_user
from app.schemas.user import UserSimpleRespVO

@router.get("/simple-list", response_model=CommonResult[List[UserSimpleRespVO]])
async def get_user_simple_list(db: AsyncSession = Depends(get_db), user = Depends(get_login_user)):
    users = await UserService.get_user_simple_list(db)
    return CommonResult.success(data=users)

@router.get("/export-excel", dependencies=[has_permission("system:user:export")])
@operate_log(type="用户管理", sub_type="导出用户")
async def export_user(req: UserPageReqVO = Depends(), db: AsyncSession = Depends(get_db)):
    content = await UserService.export_users(db, req)
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=user_export.xlsx"}
    )

@router.get("/get-import-template")
async def get_import_template():
    content = await UserService.get_import_template()
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=user_import_template.xlsx"}
    )

@router.post("/import", response_model=CommonResult[UserImportRespVO], dependencies=[has_permission("system:user:import")])
@operate_log(type="用户管理", sub_type="导入用户")
async def import_user(
    file: UploadFile = File(...),
    update_support: bool = Query(False, alias="updateSupport"),
    db: AsyncSession = Depends(get_db)
):
    content = await file.read()
    result = await UserService.import_users(db, content, update_support)
    return CommonResult.success(data=result)
