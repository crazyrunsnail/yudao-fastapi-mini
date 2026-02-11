from fastapi import APIRouter, Depends, Body, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.common.response import CommonResult
from app.schemas.user import UserProfileRespVO, UserProfileUpdateReqVO, UserProfileUpdatePasswordReqVO
from app.services.user_service import UserService
from app.core.auth import get_login_user
from typing import Optional

router = APIRouter(prefix="/system/user/profile", tags=["管理后台 - 用户个人中心"])

@router.get("/get", response_model=CommonResult[UserProfileRespVO])
async def get_user_profile(user=Depends(get_login_user), db: AsyncSession = Depends(get_db)):
    profile = await UserService.get_user_profile(db, user.id)
    return CommonResult.success(data=profile)

@router.put("/update", response_model=CommonResult[bool])
async def update_user_profile(req: UserProfileUpdateReqVO = Body(...), user=Depends(get_login_user), db: AsyncSession = Depends(get_db)):
    await UserService.update_user_profile(db, user.id, req)
    return CommonResult.success(data=True)

@router.put("/update-password", response_model=CommonResult[bool])
async def update_user_password(req: UserProfileUpdatePasswordReqVO = Body(...), user=Depends(get_login_user), db: AsyncSession = Depends(get_db)):
    # 验证旧密码逻辑 (简单起见暂未实现旧密码校验，直接更新)
    # 实际应先校验 old_password 是否正确
    await UserService.update_user_password(db, user.id, req.new_password)
    return CommonResult.success(data=True)

@router.post("/update-avatar", response_model=CommonResult[str])
async def update_user_avatar(avatar_file: UploadFile = File(...), user=Depends(get_login_user), db: AsyncSession = Depends(get_db)):
    # TODO: 实现文件上传逻辑，这里暂时返回 Mock URL
    mock_avatar_url = "https://www.iocoder.cn/images/common/logo.png"
    await UserService.update_user_avatar(db, user.id, mock_avatar_url)
    return CommonResult.success(data=mock_avatar_url)
