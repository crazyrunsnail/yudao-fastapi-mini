from sqlalchemy import String, SmallInteger, BigInteger, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base
from datetime import datetime
from typing import Optional

class SystemTenant(Base):
    __tablename__ = "system_tenant"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, comment="租户编号")
    name: Mapped[str] = mapped_column(String(63), nullable=False, comment="租户名")
    contact_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, comment="联系人编号")
    contact_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="联系人姓名")
    contact_mobile: Mapped[Optional[str]] = mapped_column(String(11), comment="联系手机")
    status: Mapped[int] = mapped_column(SmallInteger, default=0, comment="租户状态（0正常 1停用）")
    websites: Mapped[Optional[str]] = mapped_column(String(1024), default="", comment="绑定域名")
    package_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="租户套餐编号")
    expire_time: Mapped[datetime] = mapped_column(nullable=False, comment="过期时间")
    account_count: Mapped[int] = mapped_column(nullable=False, comment="账号配额")
    creator: Mapped[Optional[str]] = mapped_column(String(64), default="", comment="创建者")
    create_time: Mapped[datetime] = mapped_column(default=datetime.now, comment="创建时间")
    updater: Mapped[Optional[str]] = mapped_column(String(64), default="", comment="更新者")
    update_time: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, comment="更新时间")
    deleted: Mapped[int] = mapped_column(SmallInteger, default=0, comment="是否删除")

class SystemTenantPackage(Base):
    __tablename__ = "system_tenant_package"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, comment="套餐编号")
    name: Mapped[str] = mapped_column(String(30), nullable=False, comment="套餐名")
    status: Mapped[int] = mapped_column(SmallInteger, default=0, comment="状态（0正常 1停用）")
    menu_ids: Mapped[str] = mapped_column(String(2048), nullable=False, comment="关联的菜单编号")
    remark: Mapped[Optional[str]] = mapped_column(String(256), comment="备注")
    creator: Mapped[Optional[str]] = mapped_column(String(64), default="", comment="创建者")
    create_time: Mapped[datetime] = mapped_column(default=datetime.now, comment="创建时间")
    updater: Mapped[Optional[str]] = mapped_column(String(64), default="", comment="更新者")
    update_time: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, comment="更新时间")
    deleted: Mapped[int] = mapped_column(SmallInteger, default=0, comment="是否删除")
