from fastapi import APIRouter, Depends, Query, Body, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.dict import (
    DictDataPageReqVO, DictDataRespVO, DictDataSaveReqVO, DictDataSimpleRespVO
)
from app.services.dict_service import DictDataService
from app.common.response import CommonResult
from app.schemas.base import PageResult
from typing import List
from app.core.auth import get_login_user, has_permission
from app.common.operate_log import operate_log

router = APIRouter(prefix="/system/dict-data", tags=["管理后台 - 字典数据"])

@router.get("/page", response_model=CommonResult[PageResult[DictDataRespVO]])
@operate_log(type="字典数据", sub_type="查询字典数据分页")
async def get_dict_data_page(request: Request, req: DictDataPageReqVO = Depends(), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    items, total = await DictDataService.get_dict_data_page(db, req)
    return CommonResult.success(data=PageResult(list=items, total=total))

@router.get("/get", response_model=CommonResult[DictDataRespVO])
@operate_log(type="字典数据", sub_type="查看字典数据详情", biz_id_field="id")
async def get_dict_data(request: Request, id: int = Query(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    item = await DictDataService.get_dict_data(db, id)
    return CommonResult.success(data=item)

@router.post("/create", response_model=CommonResult[int])
@operate_log(type="字典数据", sub_type="新增字典数据")
async def create_dict_data(request: Request, req: DictDataSaveReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    item = await DictDataService.create_dict_data(db, req)
    return CommonResult.success(data=item.id)

@router.put("/update", response_model=CommonResult[bool])
@operate_log(type="字典数据", sub_type="修改字典数据")
async def update_dict_data(request: Request, req: DictDataSaveReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    await DictDataService.update_dict_data(db, req)
    return CommonResult.success(data=True)

@router.delete("/delete", response_model=CommonResult[bool])
@operate_log(type="字典数据", sub_type="删除字典数据", biz_id_field="id")
async def delete_dict_data(request: Request, id: int = Query(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    await DictDataService.delete_dict_data(db, id)
    return CommonResult.success(data=True)



@router.get("/simple-list", response_model=CommonResult[List[DictDataSimpleRespVO]])
async def get_simple_dict_data_list(db: AsyncSession = Depends(get_db), user = Depends(get_login_user)):
    items = await DictDataService.get_simple_dict_data(db)
    return CommonResult.success(data=items)

@router.get("/export-excel", dependencies=[has_permission("system:dict:export")])
@operate_log(type="字典数据", sub_type="导出字典数据")
async def export_dict_data(req: DictDataPageReqVO = Depends(), db: AsyncSession = Depends(get_db)):
    content = await DictDataService.export_dict_data(db, req)
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=dict_data_export.xlsx"}
    )
