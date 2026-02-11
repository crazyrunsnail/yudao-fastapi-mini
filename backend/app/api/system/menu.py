from fastapi import APIRouter, Depends, Query, Body, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.menu import MenuRespVO, MenuSaveReqVO, MenuSimpleRespVO
from app.services.menu_service import MenuService
from app.common.response import CommonResult
from typing import List
from app.core.auth import get_login_user
from app.common.operate_log import operate_log

router = APIRouter(prefix="/system/menu", tags=["管理后台 - 菜单"])

@router.get("/list", response_model=CommonResult[List[MenuRespVO]])
@operate_log(type="菜单管理", sub_type="查询菜单列表")
async def get_menu_list(request: Request, name: str = Query(None), status: int = Query(None), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    result = await MenuService.get_menu_list(db, name, status)
    return CommonResult.success(data=result)

@router.get("/get", response_model=CommonResult[MenuRespVO])
@operate_log(type="菜单管理", sub_type="查看菜单详情", biz_id_field="id")
async def get_menu(request: Request, id: int = Query(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    menu = await MenuService.get_menu(db, id)
    return CommonResult.success(data=menu)

@router.post("/create", response_model=CommonResult[int])
@operate_log(type="菜单管理", sub_type="新增菜单")
async def create_menu(request: Request, req: MenuSaveReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    menu_id = await MenuService.create_menu(db, req)
    return CommonResult.success(data=menu_id)

@router.put("/update", response_model=CommonResult[bool])
@operate_log(type="菜单管理", sub_type="修改菜单")
async def update_menu(request: Request, req: MenuSaveReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    await MenuService.update_menu(db, req)
    return CommonResult.success(data=True)

@router.delete("/delete", response_model=CommonResult[bool])
@operate_log(type="菜单管理", sub_type="删除菜单", biz_id_field="id")
async def delete_menu(request: Request, id: int = Query(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    await MenuService.delete_menu(db, id)
    return CommonResult.success(data=True)

@router.get("/simple-list", response_model=CommonResult[List[MenuSimpleRespVO]])
async def get_menu_simple_list(db: AsyncSession = Depends(get_db)):
    menus = await MenuService.get_all_menus(db)
    return CommonResult.success(data=menus)
