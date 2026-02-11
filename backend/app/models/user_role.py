from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseDO

class SystemUserRole(BaseDO):
    __tablename__ = "system_user_role"

    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="用户ID")
    role_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="角色ID")
