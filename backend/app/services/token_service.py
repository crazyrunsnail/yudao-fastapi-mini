import uuid
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.oauth2 import OAuth2AccessToken, OAuth2RefreshToken, OAuth2Client
from app.core.config import settings
from app.core.redis import redis_client
import json

class TokenService:
    @staticmethod
    async def create_access_token(db: AsyncSession, user_id: int, user_type: int, client_id: str):
        # 1. 获取客户端信息
        result = await db.execute(select(OAuth2Client).where(OAuth2Client.client_id == client_id))
        client = result.scalar_one_or_none()
        if not client:
            raise Exception("客户端不存在")

        # 2. 生成 token 字符串
        access_token_str = str(uuid.uuid4()).replace("-", "")
        refresh_token_str = str(uuid.uuid4()).replace("-", "")

        # 3. 计算过期时间
        expires_time = datetime.now() + timedelta(seconds=client.access_token_validity_seconds)
        refresh_expires_time = datetime.now() + timedelta(seconds=client.refresh_token_validity_seconds)

        # 4. 创建刷新令牌
        refresh_token = OAuth2RefreshToken(
            user_id=user_id,
            user_type=user_type,
            refresh_token=refresh_token_str,
            client_id=client_id,
            expires_time=refresh_expires_time,
            tenant_id=0 # 默认租户
        )
        db.add(refresh_token)
        await db.flush()

        # 5. 创建访问令牌
        access_token = OAuth2AccessToken(
            user_id=user_id,
            user_type=user_type,
            access_token=access_token_str,
            refresh_token=refresh_token_str,
            client_id=client_id,
            expires_time=expires_time,
            user_info="{}", # 暂时留空
            tenant_id=0
        )
        db.add(access_token)
        await db.commit()

        # 6. 写入 Redis 缓存
        # 模拟 java 的 RedisKeyDefine
        redis_key = f"oauth2_access_token:{access_token_str}"
        token_data = {
            "userId": user_id,
            "userType": user_type,
            "clientId": client_id,
            "expiresTime": expires_time.isoformat()
        }
        await redis_client.set(redis_key, json.dumps(token_data), ex=client.access_token_validity_seconds)

        return access_token

    @staticmethod
    async def get_access_token(db: AsyncSession, access_token: str):
        # 先查 Redis
        redis_key = f"oauth2_access_token:{access_token}"
        cached = await redis_client.get(redis_key)
        if cached:
            return json.loads(cached)

        # 再查数据库
        result = await db.execute(select(OAuth2AccessToken).where(OAuth2AccessToken.access_token == access_token))
        token = result.scalar_one_or_none()
        if token and token.expires_time > datetime.now():
            # 回填缓存
            token_data = {
                "userId": token.user_id,
                "userType": token.user_type,
                "clientId": token.client_id,
                "expiresTime": token.expires_time.isoformat()
            }
            # 计算剩余时间
            ttl = int((token.expires_time - datetime.now()).total_seconds())
            if ttl > 0:
                await redis_client.set(redis_key, json.dumps(token_data), ex=ttl)
            return token_data
        return None

    @staticmethod
    async def remove_access_token(db: AsyncSession, access_token: str):
        # 删除数据库
        await db.execute(delete(OAuth2AccessToken).where(OAuth2AccessToken.access_token == access_token))
        # 删除 Redis
        await redis_client.delete(f"oauth2_access_token:{access_token}")
        await db.commit()
    @staticmethod
    async def refresh_access_token(db: AsyncSession, refresh_token_str: str):
        # 1. 查询刷新令牌
        result = await db.execute(select(OAuth2RefreshToken).where(OAuth2RefreshToken.refresh_token == refresh_token_str))
        refresh_token = result.scalar_one_or_none()
        if not refresh_token:
            raise Exception("刷新令牌不存在")
            
        if refresh_token.expires_time < datetime.now():
            raise Exception("刷新令牌已过期")

        # 2. 创建新 access token
        return await TokenService.create_access_token(
            db, refresh_token.user_id, refresh_token.user_type, refresh_token.client_id
        )
