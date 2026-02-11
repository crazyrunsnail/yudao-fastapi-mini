from sqlalchemy import String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseDO
from typing import Optional

class SystemPost(BaseDO):
    __tablename__ = "system_post"

    code: Mapped[str] = mapped_column(String(64), nullable=False, comment="岗位编码")
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="岗位名称")
    sort: Mapped[int] = mapped_column(comment="显示顺序")
    status: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="状态（0正常 1停用）")
    remark: Mapped[Optional[str]] = mapped_column(String(500), comment="备注")
