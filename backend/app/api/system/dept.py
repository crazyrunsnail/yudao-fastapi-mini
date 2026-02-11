from fastapi import APIRouter, Depends, Query, Body, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.common.response import CommonResult
from app.schemas.dept import DeptListReqVO, DeptRespVO, DeptSaveReqVO, DeptSimpleRespVO
from app.services.dept_service import DeptService
from app.core.auth import has_permission, get_login_user
from app.common.operate_log import operate_log
from typing import List

router = APIRouter(prefix="/system/dept", tags=["管理后台 - 部门"])

@router.get("/list", response_model=CommonResult[List[DeptRespVO]], dependencies=[has_permission("system:dept:query")])
@operate_log(type="部门管理", sub_type="查询部门列表")
async def get_dept_list(request: Request, req: DeptListReqVO = Depends(), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    items = await DeptService.get_dept_list(db, req)
    return CommonResult.success(data=items)

@router.get("/get", response_model=CommonResult[DeptRespVO], dependencies=[has_permission("system:dept:query")])
@operate_log(type="部门管理", sub_type="查看部门详情", biz_id_field="id")
async def get_dept(request: Request, id: int = Query(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    item = await DeptService.get_dept(db, id)
    return CommonResult.success(data=item)

@router.post("/create", response_model=CommonResult[int], dependencies=[has_permission("system:dept:create")])
@operate_log(type="部门管理", sub_type="新增部门")
async def create_dept(request: Request, req: DeptSaveReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    item = await DeptService.create_dept(db, req)
    return CommonResult.success(data=item.id)

@router.put("/update", response_model=CommonResult[bool], dependencies=[has_permission("system:dept:update")])
@operate_log(type="部门管理", sub_type="修改部门")
async def update_dept(request: Request, req: DeptSaveReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    await DeptService.update_dept(db, req)
    return CommonResult.success(data=True)

@router.delete("/delete", response_model=CommonResult[bool], dependencies=[has_permission("system:dept:delete")])
@operate_log(type="部门管理", sub_type="删除部门", biz_id_field="id")
async def delete_dept(request: Request, id: int = Query(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    await DeptService.delete_dept(db, id)
    return CommonResult.success(data=True)

@router.get("/simple-list", response_model=CommonResult[List[DeptSimpleRespVO]])
async def get_dept_simple_list(db: AsyncSession = Depends(get_db)):
    items = await DeptService.get_dept_simple_list(db)
    return CommonResult.success(data=items)

@router.get("/export-excel", dependencies=[has_permission("system:dept:export")])
@operate_log(type="部门管理", sub_type="导出部门")
async def export_dept(req: DeptListReqVO = Depends(), db: AsyncSession = Depends(get_db)):
    content = await DeptService.export_depts(db, req)
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=dept_export.xlsx"}
    )
