from sqlalchemy import String, Integer, BigInteger, DateTime, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base
from datetime import datetime
from typing import Optional

class SystemNotifyMessage(Base):
    __tablename__ = "system_notify_message"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, comment="用户ID")
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="用户id")
    user_type: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户类型")
    template_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="模版编号")
    template_code: Mapped[str] = mapped_column(String(64), nullable=False, comment="模板编码")
    template_nickname: Mapped[Optional[str]] = mapped_column(String(64), comment="模版发送人名称")
    template_content: Mapped[str] = mapped_column(Text, nullable=False, comment="模版内容")
    template_type: Mapped[int] = mapped_column(Integer, nullable=False, comment="模版类型")
    template_params: Mapped[str] = mapped_column(Text, nullable=False, comment="模版参数")
    read_status: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否已读")
    read_time: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="阅读时间")
    
    creator: Mapped[Optional[str]] = mapped_column(String(64), default="", comment="创建者")
    create_time: Mapped[datetime] = mapped_column(default=datetime.now, comment="创建时间")
    updater: Mapped[Optional[str]] = mapped_column(String(64), default="", comment="更新者")
    update_time: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, comment="更新时间")
    deleted: Mapped[int] = mapped_column(Integer, default=0, comment="是否删除")
    tenant_id: Mapped[int] = mapped_column(BigInteger, default=0, comment="租户编号")

class SystemNotifyTemplate(Base):
    __tablename__ = "system_notify_template"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, comment="编号")
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="模板名称")
    code: Mapped[str] = mapped_column(String(64), nullable=False, comment="模板编码")
    nickname: Mapped[str] = mapped_column(String(64), nullable=False, comment="发送人名称")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="模板内容")
    type: Mapped[int] = mapped_column(Integer, nullable=False, comment="模板类型")
    params: Mapped[Optional[str]] = mapped_column(Text, comment="模板参数")
    status: Mapped[int] = mapped_column(Integer, default=0, comment="状态")
    remark: Mapped[Optional[str]] = mapped_column(String(255), comment="备注")

    creator: Mapped[Optional[str]] = mapped_column(String(64), default="", comment="创建者")
    create_time: Mapped[datetime] = mapped_column(default=datetime.now, comment="创建时间")
    updater: Mapped[Optional[str]] = mapped_column(String(64), default="", comment="更新者")
    update_time: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, comment="更新时间")
    deleted: Mapped[int] = mapped_column(Integer, default=0, comment="是否删除")
    tenant_id: Mapped[int] = mapped_column(BigInteger, default=0, comment="租户编号")
