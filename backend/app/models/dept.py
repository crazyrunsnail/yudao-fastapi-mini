from sqlalchemy import String, SmallInteger, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseDO
from typing import Optional

class SystemDept(BaseDO):
    __tablename__ = "system_dept"

    name: Mapped[str] = mapped_column(String(30), default="", comment="部门名称")
    parent_id: Mapped[int] = mapped_column(BigInteger, default=0, comment="父部门id")
    sort: Mapped[int] = mapped_column(default=0, comment="显示顺序")
    leader_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, comment="负责人")
    phone: Mapped[Optional[str]] = mapped_column(String(11), comment="联系电话")
    email: Mapped[Optional[str]] = mapped_column(String(50), comment="邮箱")
    status: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="部门状态")
