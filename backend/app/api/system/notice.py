from fastapi import APIRouter, Depends, Query, Body, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.notice import NoticePageReqVO, NoticeRespVO, NoticeCreateReqVO, NoticeUpdateReqVO
from app.services.notice_service import NoticeService
from app.common.response import CommonResult
from app.common.paging import PageResult
from app.core.auth import get_login_user
from app.common.operate_log import operate_log
from typing import List

router = APIRouter(prefix="/system/notice", tags=["管理后台 - 通知公告"])

@router.get("/page", response_model=CommonResult[PageResult[NoticeRespVO]])
@operate_log(type="通知公告", sub_type="查询公告分页")
async def get_notice_page(request: Request, req: NoticePageReqVO = Depends(), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    items, total = await NoticeService.get_notice_page(db, req)
    return CommonResult.success(data=PageResult(list=items, total=total))

@router.get("/get", response_model=CommonResult[NoticeRespVO])
@operate_log(type="通知公告", sub_type="查看公告详情", biz_id_field="id")
async def get_notice(request: Request, id: int = Query(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    notice = await NoticeService.get_notice(db, id)
    return CommonResult.success(data=notice)

@router.post("/create", response_model=CommonResult[int])
@operate_log(type="通知公告", sub_type="新增公告")
async def create_notice(request: Request, req: NoticeCreateReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    notice_id = await NoticeService.create_notice(db, req)
    return CommonResult.success(data=notice_id)

@router.put("/update", response_model=CommonResult[bool])
@operate_log(type="通知公告", sub_type="修改公告")
async def update_notice(request: Request, req: NoticeUpdateReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    await NoticeService.update_notice(db, req)
    return CommonResult.success(data=True)

@router.delete("/delete", response_model=CommonResult[bool])
@operate_log(type="通知公告", sub_type="删除公告", biz_id_field="id")
async def delete_notice(request: Request, id: int = Query(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    await NoticeService.delete_notice(db, id)
    return CommonResult.success(data=True)
