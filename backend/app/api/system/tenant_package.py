from fastapi import APIRouter, Depends, Query, Body, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.common.response import CommonResult
from app.schemas.tenant_package import TenantPackagePageReqVO, TenantPackageSaveReqVO, TenantPackageRespVO, TenantPackageSimpleRespVO
from app.services.tenant_package_service import TenantPackageService
from app.schemas.base import PageResult
from typing import List
from app.core.auth import has_permission

router = APIRouter(prefix="/system/tenant-package", tags=["管理后台 - 租户套餐"])

@router.get("/page", response_model=CommonResult[PageResult[TenantPackageRespVO]], dependencies=[has_permission("system:tenant-package:query")])
async def get_tenant_package_page(req: TenantPackagePageReqVO = Depends(), db: AsyncSession = Depends(get_db)):
    result = await TenantPackageService.get_tenant_package_page(db, req)
    return CommonResult.success(data=result)

@router.get("/get", response_model=CommonResult[TenantPackageRespVO], dependencies=[has_permission("system:tenant-package:query")])
async def get_tenant_package(id: int = Query(...), db: AsyncSession = Depends(get_db)):
    item = await TenantPackageService.get_tenant_package(db, id)
    return CommonResult.success(data=item)

@router.post("/create", response_model=CommonResult[int], dependencies=[has_permission("system:tenant-package:create")])
async def create_tenant_package(req: TenantPackageSaveReqVO = Body(...), db: AsyncSession = Depends(get_db)):
    item = await TenantPackageService.create_tenant_package(db, req)
    return CommonResult.success(data=item.id)

@router.put("/update", response_model=CommonResult[bool], dependencies=[has_permission("system:tenant-package:update")])
async def update_tenant_package(req: TenantPackageSaveReqVO = Body(...), db: AsyncSession = Depends(get_db)):
    await TenantPackageService.update_tenant_package(db, req)
    return CommonResult.success(data=True)

@router.delete("/delete", response_model=CommonResult[bool], dependencies=[has_permission("system:tenant-package:delete")])
async def delete_tenant_package(id: int = Query(...), db: AsyncSession = Depends(get_db)):
    await TenantPackageService.delete_tenant_package(db, id)
    return CommonResult.success(data=True)

@router.get("/simple-list", response_model=CommonResult[List[TenantPackageSimpleRespVO]])
async def get_tenant_package_simple_list(db: AsyncSession = Depends(get_db)):
    # 租户套餐列表通常不需要复杂权限， 或者用 query 权限
    items = await TenantPackageService.get_tenant_package_simple_list(db)
    return CommonResult.success(data=items)

@router.get("/export-excel", dependencies=[has_permission("system:tenant-package:export")])
async def export_tenant_package(req: TenantPackagePageReqVO = Depends(), db: AsyncSession = Depends(get_db)):
    content = await TenantPackageService.export_tenant_packages(db, req)
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=tenant_package_export.xlsx"}
    )
