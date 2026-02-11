from sqlalchemy import String, SmallInteger, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base
from datetime import datetime
from typing import Optional

class SystemDictType(Base):
    __tablename__ = "system_dict_type"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, comment="字典主键")
    name: Mapped[str] = mapped_column(String(100), default="", comment="字典名称")
    type: Mapped[str] = mapped_column(String(100), default="", comment="字典类型")
    status: Mapped[int] = mapped_column(SmallInteger, default=0, comment="状态（0正常 1停用）")
    remark: Mapped[Optional[str]] = mapped_column(String(500), comment="备注")
    creator: Mapped[Optional[str]] = mapped_column(String(64), default="", comment="创建者")
    create_time: Mapped[datetime] = mapped_column(default=datetime.now, comment="创建时间")
    updater: Mapped[Optional[str]] = mapped_column(String(64), default="", comment="更新者")
    update_time: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, comment="更新时间")
    deleted: Mapped[int] = mapped_column(SmallInteger, default=0, comment="是否删除")
    deleted_time: Mapped[Optional[datetime]] = mapped_column(comment="删除时间")

class SystemDictData(Base):
    __tablename__ = "system_dict_data"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, comment="字典编码")
    sort: Mapped[int] = mapped_column(default=0, comment="字典排序")
    label: Mapped[str] = mapped_column(String(100), default="", comment="字典标签")
    value: Mapped[str] = mapped_column(String(100), default="", comment="字典键值")
    dict_type: Mapped[str] = mapped_column(String(100), default="", comment="字典类型")
    status: Mapped[int] = mapped_column(SmallInteger, default=0, comment="状态（0正常 1停用）")
    color_type: Mapped[Optional[str]] = mapped_column(String(100), default="", comment="颜色类型")
    css_class: Mapped[Optional[str]] = mapped_column(String(100), default="", comment="css 样式")
    remark: Mapped[Optional[str]] = mapped_column(String(500), comment="备注")
    creator: Mapped[Optional[str]] = mapped_column(String(64), default="", comment="创建者")
    create_time: Mapped[datetime] = mapped_column(default=datetime.now, comment="创建时间")
    updater: Mapped[Optional[str]] = mapped_column(String(64), default="", comment="更新者")
    update_time: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, comment="更新时间")
    deleted: Mapped[int] = mapped_column(SmallInteger, default=0, comment="是否删除")
