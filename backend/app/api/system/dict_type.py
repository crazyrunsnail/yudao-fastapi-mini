from fastapi import APIRouter, Depends, Query, Body, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.dict import (
    DictTypePageReqVO, DictTypeRespVO, DictTypeSaveReqVO, DictTypeSimpleRespVO
)
from app.services.dict_service import DictTypeService
from app.common.response import CommonResult
from app.schemas.base import PageResult
from typing import List
from app.core.auth import get_login_user, has_permission
from app.common.operate_log import operate_log

router = APIRouter(prefix="/system/dict-type", tags=["管理后台 - 字典类型"])

@router.get("/page", response_model=CommonResult[PageResult[DictTypeRespVO]])
@operate_log(type="字典类型", sub_type="查询字典类型分页")
async def get_dict_type_page(request: Request, req: DictTypePageReqVO = Depends(), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    items, total = await DictTypeService.get_dict_type_page(db, req)
    return CommonResult.success(data=PageResult(list=items, total=total))

@router.get("/get", response_model=CommonResult[DictTypeRespVO])
@operate_log(type="字典类型", sub_type="查看字典类型详情", biz_id_field="id")
async def get_dict_type(request: Request, id: int = Query(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    item = await DictTypeService.get_dict_type(db, id)
    return CommonResult.success(data=item)

@router.post("/create", response_model=CommonResult[int])
@operate_log(type="字典类型", sub_type="新增字典类型")
async def create_dict_type(request: Request, req: DictTypeSaveReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    item = await DictTypeService.create_dict_type(db, req)
    return CommonResult.success(data=item.id)

@router.put("/update", response_model=CommonResult[bool])
@operate_log(type="字典类型", sub_type="修改字典类型")
async def update_dict_type(request: Request, req: DictTypeSaveReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    await DictTypeService.update_dict_type(db, req)
    return CommonResult.success(data=True)

@router.delete("/delete", response_model=CommonResult[bool])
@operate_log(type="字典类型", sub_type="删除字典类型", biz_id_field="id")
async def delete_dict_type(request: Request, id: int = Query(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    await DictTypeService.delete_dict_type(db, id)
    return CommonResult.success(data=True)

@router.get("/simple-list", response_model=CommonResult[List[DictTypeSimpleRespVO]])
async def get_simple_dict_type_list(db: AsyncSession = Depends(get_db)):
    items = await DictTypeService.get_all_dict_types(db)
    return CommonResult.success(data=items)

@router.get("/export-excel", dependencies=[has_permission("system:dict:export")])
@operate_log(type="字典类型", sub_type="导出字典类型")
async def export_dict_type(req: DictTypePageReqVO = Depends(), db: AsyncSession = Depends(get_db)):
    content = await DictTypeService.export_dict_types(db, req)
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=dict_type_export.xlsx"}
    )
