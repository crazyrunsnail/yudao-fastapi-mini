from fastapi import APIRouter, Depends, Query, Body, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.common.response import CommonResult
from sqlalchemy import select
from app.models.tenant import SystemTenant
from app.schemas.tenant import TenantPageReqVO, TenantRespVO, TenantSaveReqVO
from app.schemas.base import PageResult
from app.services.tenant_service import TenantService
from app.core.auth import has_permission, get_login_user

router = APIRouter(prefix="/system/tenant", tags=["管理后台 - 租户"])

@router.get("/page", response_model=CommonResult[PageResult[TenantRespVO]], dependencies=[has_permission("system:tenant:query")])
async def get_tenant_page(req: TenantPageReqVO = Depends(), db: AsyncSession = Depends(get_db)):
    result = await TenantService.get_tenant_page(db, req)
    return CommonResult.success(data=result)

@router.get("/get", response_model=CommonResult[TenantRespVO], dependencies=[has_permission("system:tenant:query")])
async def get_tenant(id: int = Query(...), db: AsyncSession = Depends(get_db)):
    item = await TenantService.get_tenant(db, id)
    return CommonResult.success(data=item)

@router.post("/create", response_model=CommonResult[int], dependencies=[has_permission("system:tenant:create")])
async def create_tenant(req: TenantSaveReqVO = Body(...), db: AsyncSession = Depends(get_db)):
    item = await TenantService.create_tenant(db, req)
    return CommonResult.success(data=item.id)

@router.put("/update", response_model=CommonResult[bool], dependencies=[has_permission("system:tenant:update")])
async def update_tenant(req: TenantSaveReqVO = Body(...), db: AsyncSession = Depends(get_db)):
    await TenantService.update_tenant(db, req)
    return CommonResult.success(data=True)

@router.delete("/delete", response_model=CommonResult[bool], dependencies=[has_permission("system:tenant:delete")])
async def delete_tenant(id: int = Query(...), db: AsyncSession = Depends(get_db)):
    await TenantService.delete_tenant(db, id)
    return CommonResult.success(data=True)

@router.get("/get-id-by-name")
async def get_tenant_id_by_name(name: str = Query(...), db: AsyncSession = Depends(get_db)):
    # 暂时默认返回 1，或者根据名称查询
    stmt = select(SystemTenant.id).where(SystemTenant.name == name, SystemTenant.deleted == 0)
    result = await db.execute(stmt)
    tenant_id = result.scalar_one_or_none()
    
    # 如果找不到，为了兼容前端演示，可以返回默认值 1，或者空
    if tenant_id is None:
        # 在 seed 数据还没完善前，如果找不到就返回 1
        return CommonResult.success(data=1)
    
    return CommonResult.success(data=tenant_id)

from app.core.auth import get_login_user

@router.get("/simple-list")
async def get_tenant_simple_list(db: AsyncSession = Depends(get_db), user = Depends(get_login_user)): 
    # Mock 返回
    return CommonResult.success(data=[{"id": 1, "name": "yudao"}])

@router.get("/get-by-website")
async def get_tenant_by_website(website: str = Query(...), db: AsyncSession = Depends(get_db)):
    # 暂时 Mock 返回
    return CommonResult.success(data={
        "id": 1,
        "name": "yudao",
        "logo": ""
    })

@router.get("/export-excel", dependencies=[has_permission("system:tenant:export")])
async def export_tenant(req: TenantPageReqVO = Depends(), db: AsyncSession = Depends(get_db)):
    content = await TenantService.export_tenants(db, req)
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=tenant_export.xlsx"}
    )
