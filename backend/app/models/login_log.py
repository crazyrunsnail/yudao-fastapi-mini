from sqlalchemy import String, SmallInteger, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseDO
from datetime import datetime
from typing import Optional

class SystemLoginLog(BaseDO):
    __tablename__ = "system_login_log"

    log_type: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="日志类型")
    trace_id: Mapped[str] = mapped_column(String(64), default="", comment="链路追踪编号")
    username: Mapped[str] = mapped_column(String(50), default="", comment="用户账号")
    user_ip: Mapped[Optional[str]] = mapped_column(String(50), default="", comment="用户 IP")
    user_agent: Mapped[Optional[str]] = mapped_column(String(512), default="", comment="浏览器 UA")
    result: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="登录结果")
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger, comment="用户编号")
    user_type: Mapped[int] = mapped_column(SmallInteger, default=0, comment="用户类型")
