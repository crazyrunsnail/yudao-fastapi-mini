from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.common.response import CommonResult
from app.schemas.notify import (
    NotifyTemplateCreateReqVO, NotifyTemplateUpdateReqVO, 
    NotifyTemplateRespVO, NotifyTemplatePageReqVO, NotifySendReqVO
)
from app.services.notify_service import NotifyTemplateService, NotifyService
from app.common.paging import PageResult
from app.core.auth import get_login_user
from typing import List

router = APIRouter(prefix="/system/notify-template", tags=["管理后台 - 站内信模板"])

@router.post("/", response_model=CommonResult[int])
async def create_notify_template(req: NotifyTemplateCreateReqVO = Body(...), db: AsyncSession = Depends(get_db)):
    template_id = await NotifyTemplateService.create_template(db, req)
    return CommonResult.success(data=template_id)

@router.put("/", response_model=CommonResult[bool])
async def update_notify_template(req: NotifyTemplateUpdateReqVO = Body(...), db: AsyncSession = Depends(get_db)):
    await NotifyTemplateService.update_template(db, req)
    return CommonResult.success(data=True)

@router.delete("/", response_model=CommonResult[bool])
async def delete_notify_template(id: int = Query(...), db: AsyncSession = Depends(get_db)):
    await NotifyTemplateService.delete_template(db, id)
    return CommonResult.success(data=True)

@router.get("/get", response_model=CommonResult[NotifyTemplateRespVO])
async def get_notify_template(id: int = Query(...), db: AsyncSession = Depends(get_db)):
    template = await NotifyTemplateService.get_template(db, id)
    return CommonResult.success(data=template)

@router.get("/page", response_model=CommonResult[PageResult[NotifyTemplateRespVO]])
async def get_notify_template_page(req: NotifyTemplatePageReqVO = Depends(), db: AsyncSession = Depends(get_db)):
    items, total = await NotifyTemplateService.get_template_page(db, req)
    return CommonResult.success(data=PageResult(list=items, total=total))

@router.post("/send-notify", response_model=CommonResult[int])
async def send_test_notify(
    req: NotifySendReqVO = Body(...),
    db: AsyncSession = Depends(get_db)
):
    msg_id = await NotifyService.send_single_notify(db, req.user_id, req.template_code, req.template_params)
    return CommonResult.success(data=msg_id)
