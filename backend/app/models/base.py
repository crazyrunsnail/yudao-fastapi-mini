from datetime import datetime
from typing import Optional
from sqlalchemy import Column, BigInteger, String, DateTime, SmallInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class BaseDO(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, comment="主键")
    creator: Mapped[Optional[str]] = mapped_column(String(64), default="", comment="创建者")
    create_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updater: Mapped[Optional[str]] = mapped_column(String(64), default="", onupdate="", comment="更新者")
    update_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    deleted: Mapped[int] = mapped_column(SmallInteger, default=0, comment="是否删除")
    tenant_id: Mapped[int] = mapped_column(BigInteger, default=0, comment="租户编号")

