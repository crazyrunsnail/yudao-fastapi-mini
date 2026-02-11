from sqlalchemy import Column, BigInteger, String, SmallInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseDO
from datetime import datetime
from typing import Optional

class SystemUser(BaseDO):
    __tablename__ = "system_users"

    username: Mapped[str] = mapped_column(String(30), nullable=False, comment="用户账号")
    password: Mapped[str] = mapped_column(String(100), default="", comment="密码")
    nickname: Mapped[str] = mapped_column(String(30), nullable=False, comment="用户昵称")
    remark: Mapped[Optional[str]] = mapped_column(String(500), comment="备注")
    dept_id: Mapped[Optional[int]] = mapped_column(BigInteger, comment="部门ID")
    post_ids: Mapped[Optional[str]] = mapped_column(String(255), comment="岗位编号数组")
    email: Mapped[Optional[str]] = mapped_column(String(50), default="", comment="用户邮箱")
    mobile: Mapped[Optional[str]] = mapped_column(String(11), default="", comment="手机号码")
    sex: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0, comment="用户性别")
    avatar: Mapped[Optional[str]] = mapped_column(String(512), default="", comment="头像地址")
    status: Mapped[int] = mapped_column(SmallInteger, default=0, comment="帐号状态（0正常 1停用）")
    login_ip: Mapped[Optional[str]] = mapped_column(String(50), default="", comment="最后登录IP")
    login_date: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="最后登录时间")
