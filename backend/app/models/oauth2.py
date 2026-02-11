from sqlalchemy import String, SmallInteger, BigInteger, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseDO, Base
from datetime import datetime
from typing import Optional

class OAuth2AccessToken(BaseDO):
    __tablename__ = "system_oauth2_access_token"

    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="用户编号")
    user_type: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="用户类型")
    user_info: Mapped[str] = mapped_column(String(512), nullable=False, comment="用户信息")
    access_token: Mapped[str] = mapped_column(String(255), nullable=False, comment="访问令牌")
    refresh_token: Mapped[str] = mapped_column(String(32), nullable=False, comment="刷新令牌")
    client_id: Mapped[str] = mapped_column(String(255), nullable=False, comment="客户端编号")
    scopes: Mapped[Optional[str]] = mapped_column(String(255), comment="授权范围")
    expires_time: Mapped[datetime] = mapped_column(nullable=False, comment="过期时间")

class OAuth2RefreshToken(BaseDO):
    __tablename__ = "system_oauth2_refresh_token"

    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="用户编号")
    refresh_token: Mapped[str] = mapped_column(String(32), nullable=False, comment="刷新令牌")
    user_type: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="用户类型")
    client_id: Mapped[str] = mapped_column(String(255), nullable=False, comment="客户端编号")
    scopes: Mapped[Optional[str]] = mapped_column(String(255), comment="授权范围")
    expires_time: Mapped[datetime] = mapped_column(nullable=False, comment="过期时间")

class OAuth2Client(Base):
    __tablename__ = "system_oauth2_client"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, comment="编号")
    client_id: Mapped[str] = mapped_column(String(255), nullable=False, comment="客户端编号")
    secret: Mapped[str] = mapped_column(String(255), nullable=False, comment="客户端密钥")
    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="应用名")
    logo: Mapped[str] = mapped_column(String(255), nullable=False, comment="应用图标")
    description: Mapped[Optional[str]] = mapped_column(String(255), comment="应用描述")
    status: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="状态")
    access_token_validity_seconds: Mapped[int] = mapped_column(nullable=False, comment="访问令牌的有效期")
    refresh_token_validity_seconds: Mapped[int] = mapped_column(nullable=False, comment="刷新令牌的有效期")
    redirect_uris: Mapped[str] = mapped_column(String(255), nullable=False, comment="可重定向的 URI 地址")
    authorized_grant_types: Mapped[str] = mapped_column(String(255), nullable=False, comment="授权类型")
    scopes: Mapped[Optional[str]] = mapped_column(String(255), comment="授权范围")
    auto_approve_scopes: Mapped[Optional[str]] = mapped_column(String(255), comment="自动通过的授权范围")
    authorities: Mapped[Optional[str]] = mapped_column(String(255), comment="权限")
    resource_ids: Mapped[Optional[str]] = mapped_column(String(255), comment="资源")
    additional_information: Mapped[Optional[str]] = mapped_column(String(4096), comment="附加信息")
    creator: Mapped[Optional[str]] = mapped_column(String(64), default="", comment="创建者")
    create_time: Mapped[datetime] = mapped_column(default=datetime.now, comment="创建时间")
    updater: Mapped[Optional[str]] = mapped_column(String(64), default="", comment="更新者")
    update_time: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, comment="更新时间")
    deleted: Mapped[int] = mapped_column(SmallInteger, default=0, comment="是否删除")
