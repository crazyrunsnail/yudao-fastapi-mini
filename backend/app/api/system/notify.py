from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.common.response import CommonResult
from app.schemas.notify import NotifyMessageMyPageReqVO, NotifyMessageRespVO, NotifyMessagePageReqVO
from app.services.notify_service import NotifyService
from app.common.paging import PageResult
from app.core.auth import get_login_user
from typing import List

router = APIRouter(prefix="/system/notify-message", tags=["管理后台 - 站内信"])

@router.get("/my-page", response_model=CommonResult[PageResult[NotifyMessageRespVO]])
async def get_my_notify_message_page(req: NotifyMessageMyPageReqVO = Depends(), user=Depends(get_login_user), db: AsyncSession = Depends(get_db)):
    items, total = await NotifyService.get_my_page(db, req, user.id)
    return CommonResult.success(data=PageResult(list=items, total=total))

@router.get("/get-unread-count", response_model=CommonResult[int])
async def get_unread_count(user=Depends(get_login_user), db: AsyncSession = Depends(get_db)):
    count = await NotifyService.get_unread_count(db, user.id)
    return CommonResult.success(data=count)

@router.put("/update-read", response_model=CommonResult[bool])
async def update_notify_message_read(ids: List[int] = Body(...), user=Depends(get_login_user), db: AsyncSession = Depends(get_db)):
    await NotifyService.update_read(db, ids, user.id)
    return CommonResult.success(data=True)

@router.put("/update-all-read", response_model=CommonResult[bool])
async def update_all_notify_message_read(user=Depends(get_login_user), db: AsyncSession = Depends(get_db)):
    await NotifyService.update_all_read(db, user.id)
    return CommonResult.success(data=True)
@router.get("/page", response_model=CommonResult[PageResult[NotifyMessageRespVO]])
async def get_notify_message_page(req: NotifyMessagePageReqVO = Depends(), db: AsyncSession = Depends(get_db)):
    items, total = await NotifyService.get_notify_message_page(db, req)
    return CommonResult.success(data=PageResult(list=items, total=total))

@router.get("/get-unread-list", response_model=CommonResult[List[NotifyMessageRespVO]])
async def get_unread_notify_message_list(size: int = Query(10), user=Depends(get_login_user), db: AsyncSession = Depends(get_db)):
    items = await NotifyService.get_unread_list(db, user.id, size)
    return CommonResult.success(data=items)
