from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.log import LoginLogPageReqVO, LoginLogRespVO
from app.services.log_service import LogService
from app.common.response import CommonResult
from app.schemas.base import PageResult

router = APIRouter(prefix="/system/login-log", tags=["管理后台 - 登录日志"])

@router.get("/page", response_model=CommonResult[PageResult[LoginLogRespVO]])
async def get_login_log_page(req: LoginLogPageReqVO = Depends(), db: AsyncSession = Depends(get_db)):
    items, total = await LogService.get_login_log_page(db, req)
    return CommonResult.success(data=PageResult(list=items, total=total))

@router.get("/export-excel")
async def export_login_log(req: LoginLogPageReqVO = Depends(), db: AsyncSession = Depends(get_db)):
    content = await LogService.export_login_logs(db, req)
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=login_log_export.xlsx"}
    )
