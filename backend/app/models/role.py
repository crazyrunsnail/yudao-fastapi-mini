from sqlalchemy import String, SmallInteger, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseDO
from typing import Optional

class SystemRole(BaseDO):
    __tablename__ = "system_role"

    name: Mapped[str] = mapped_column(String(30), nullable=False, comment="角色名称")
    code: Mapped[str] = mapped_column(String(100), nullable=False, comment="角色权限字符串")
    sort: Mapped[int] = mapped_column(comment="显示顺序")
    data_scope: Mapped[int] = mapped_column(SmallInteger, default=1, comment="数据范围")
    data_scope_dept_ids: Mapped[str] = mapped_column(String(500), default="", comment="数据范围(指定部门数组)")
    status: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="角色状态")
    type: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="角色类型")
    remark: Mapped[Optional[str]] = mapped_column(String(500), comment="备注")
