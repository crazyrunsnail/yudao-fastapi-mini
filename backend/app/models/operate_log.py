from sqlalchemy import String, SmallInteger, BigInteger, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseDO
from datetime import datetime
from typing import Optional

class SystemOperateLog(BaseDO):
    __tablename__ = "system_operate_log"

    trace_id: Mapped[str] = mapped_column(String(64), default="", comment="链路追踪编号")
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="用户编号")
    user_type: Mapped[int] = mapped_column(SmallInteger, default=0, comment="用户类型")
    type: Mapped[str] = mapped_column(String(50), nullable=False, comment="操作模块类型")
    sub_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="操作名")
    biz_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="操作模块业务编号")
    action: Mapped[str] = mapped_column(String(2000), default="", comment="操作内容")
    success: Mapped[bool] = mapped_column(default=True, comment="操作结果")
    extra: Mapped[str] = mapped_column(String(2000), default="", comment="拓展字段")
    request_method: Mapped[Optional[str]] = mapped_column(String(16), default="", comment="请求方法名")
    request_url: Mapped[Optional[str]] = mapped_column(String(255), default="", comment="请求地址")
    user_ip: Mapped[Optional[str]] = mapped_column(String(50), default="", comment="用户 IP")
    user_agent: Mapped[Optional[str]] = mapped_column(String(512), default="", comment="浏览器 UA")
