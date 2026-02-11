from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import SystemUser
from app.core.security import verify_password
from app.services.token_service import TokenService
from app.schemas.auth import AuthLoginReqVO, AuthLoginRespVO
from fastapi import HTTPException

class AuthService:
    @staticmethod
    async def login(db: AsyncSession, req: AuthLoginReqVO):
        # 1. 查询用户
        result = await db.execute(select(SystemUser).where(SystemUser.username == req.username))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=400, detail="账号不存在")
        
        # 2. 校验密码
        if not verify_password(req.password, user.password):
            raise HTTPException(status_code=400, detail="密码错误")
        
        # 3. 校验状态
        if user.status != 0:
            raise HTTPException(status_code=400, detail="账号已被禁用")

        # 4. 创建 Token
        # 默认 client_id 为 "default"
        token = await TokenService.create_access_token(db, user.id, 1, "default")
        
        return AuthLoginRespVO(
            user_id=user.id,
            access_token=token.access_token,
            refresh_token=token.refresh_token,
            expires_time=token.expires_time
        )

    @staticmethod
    async def refresh_token(db: AsyncSession, refresh_token: str):
        try:
            token = await TokenService.refresh_access_token(db, refresh_token)
            return AuthLoginRespVO(
                user_id=token.user_id,
                access_token=token.access_token,
                refresh_token=token.refresh_token,
                expires_time=token.expires_time
            )
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))

    @staticmethod
    async def logout(db: AsyncSession, access_token: str):
        if access_token:
            await TokenService.remove_access_token(db, access_token)
