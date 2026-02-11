from sqlalchemy import String, SmallInteger, BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseDO
from typing import Optional

class SystemNotice(BaseDO):
    __tablename__ = "system_notice"

    title: Mapped[str] = mapped_column(String(50), nullable=False, comment="公告标题")
    type: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="公告类型（1通知 2公告）")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="公告内容")
    status: Mapped[int] = mapped_column(SmallInteger, default=0, comment="公告状态（0正常 1关闭）")
    remark: Mapped[Optional[str]] = mapped_column(String(255), comment="备注")
