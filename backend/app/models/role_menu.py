from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseDO

class SystemRoleMenu(BaseDO):
    __tablename__ = "system_role_menu"

    role_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="角色ID")
    menu_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="菜单ID")
