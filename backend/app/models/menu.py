from sqlalchemy import String, SmallInteger, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base # 菜单表没有 tenant_id 等，通常在 yudao 中是全局的，但有些也有。
# 查一下 SQL，system_menu 没有 tenant_id 和 creator/updater 吗？
# 回看 SQL: line 1749. 有 creator/updater，但确实没看到 tenant_id。
from app.models.base import Base
from datetime import datetime
from typing import Optional

class SystemMenu(Base):
    __tablename__ = "system_menu"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, comment="菜单ID")
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="菜单名称")
    permission: Mapped[str] = mapped_column(String(100), default="", comment="权限标识")
    type: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="菜单类型")
    sort: Mapped[int] = mapped_column(default=0, comment="显示顺序")
    parent_id: Mapped[int] = mapped_column(BigInteger, default=0, comment="父菜单ID")
    path: Mapped[Optional[str]] = mapped_column(String(200), default="", comment="路由地址")
    icon: Mapped[Optional[str]] = mapped_column(String(100), default="#", comment="菜单图标")
    component: Mapped[Optional[str]] = mapped_column(String(255), comment="组件路径")
    component_name: Mapped[Optional[str]] = mapped_column(String(255), comment="组件名")
    status: Mapped[int] = mapped_column(SmallInteger, default=0, comment="菜单状态")
    visible: Mapped[bool] = mapped_column(default=True, comment="是否可见")
    keep_alive: Mapped[bool] = mapped_column(default=True, comment="是否缓存")
    always_show: Mapped[bool] = mapped_column(default=True, comment="是否总是显示")
    creator: Mapped[Optional[str]] = mapped_column(String(64), default="", comment="创建者")
    create_time: Mapped[datetime] = mapped_column(default=datetime.now, comment="创建时间")
    updater: Mapped[Optional[str]] = mapped_column(String(64), default="", comment="更新者")
    update_time: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, comment="更新时间")
    deleted: Mapped[int] = mapped_column(SmallInteger, default=0, comment="是否删除")
