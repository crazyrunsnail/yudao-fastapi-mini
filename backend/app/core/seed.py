import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.user import SystemUser
from app.models.role import SystemRole
from app.models.oauth2 import OAuth2Client
from app.models.user_role import SystemUserRole
from app.models.dict import SystemDictData
from app.models.menu import SystemMenu
from datetime import datetime
from app.core.security import hash_password

async def seed_data():
    async with AsyncSessionLocal() as session:
        # 1. 创建超级管理员角色
        stmt = select(SystemRole).where(SystemRole.id == 1)
        role = (await session.execute(stmt)).scalar_one_or_none()
        if not role:
            role = SystemRole(
                id=1,
                name="超级管理员",
                code="super_admin",
                sort=1,
                status=0,
                type=1,
                remark="超级管理员角色",
                creator="system",
                updater="system",
                tenant_id=0
            )
            session.add(role)

        # 2. 创建管理员用户
        stmt = select(SystemUser).where(SystemUser.id == 1)
        user = (await session.execute(stmt)).scalar_one_or_none()
        if not user:
            hashed_password = hash_password("admin123")
            user = SystemUser(
                id=1,
                username="admin",
                password=hashed_password,
                nickname="超级管理员",
                status=0,
                creator="system",
                updater="system",
                tenant_id=0
            )
            session.add(user)

        # 3. 关联用户和角色
        stmt = select(SystemUserRole).where(SystemUserRole.user_id == 1, SystemUserRole.role_id == 1)
        user_role = (await session.execute(stmt)).scalar_one_or_none()
        if not user_role:
            user_role = SystemUserRole(
                user_id=1,
                role_id=1,
                creator="system",
                updater="system",
                tenant_id=0
            )
            session.add(user_role)

        # 4. 创建默认 OAuth2 客户端
        stmt = select(OAuth2Client).where(OAuth2Client.client_id == "default")
        client = (await session.execute(stmt)).scalar_one_or_none()
        if not client:
            client = OAuth2Client(
                client_id="default",
                secret="default_secret",
                name="默认客户端",
                logo="https://www.iocoder.cn/images/common/logo.png",
                status=0,
                access_token_validity_seconds=1800,
                refresh_token_validity_seconds=2592000,
                redirect_uris="http://localhost:3000",
                authorized_grant_types="password,refresh_token",
                creator="system",
                updater="system"
            )
            session.add(client)

        # 5. 基础字典数据
        dict_items = [
            ("sys_common_status", "正常", "0"),
            ("sys_common_status", "停用", "1"),
            ("sys_user_sex", "男", "1"),
            ("sys_user_sex", "女", "2"),
        ]
        for dt, label, val in dict_items:
            stmt = select(SystemDictData).where(SystemDictData.dict_type == dt, SystemDictData.value == val)
            item = (await session.execute(stmt)).scalar_one_or_none()
            if not item:
                session.add(SystemDictData(dict_type=dt, label=label, value=val, sort=1, status=0, creator="system"))

        # 6. 基础菜单数据
        # ID, Name, ParentID, Sort, Type, Path, Component, Permission, Icon, ComponentName
        menu_items = [
            (1, "系统管理", 0, 1, 1, "/system", "Layout", None, "system", "System"),
            (100, "用户管理", 1, 1, 2, "user", "system/user/index", "system:user:query", "user", "SystemUser"),
            (101, "角色管理", 1, 2, 2, "role", "system/role/index", "system:role:query", "peoples", "SystemRole"),
            (102, "菜单管理", 1, 3, 2, "menu", "system/menu/index", "system:menu:query", "tree-table", "SystemMenu"),
            (103, "部门管理", 1, 4, 2, "dept", "system/dept/index", "system:dept:query", "tree", "SystemDept"),
            (104, "岗位管理", 1, 5, 2, "post", "system/post/index", "system:post:query", "post", "SystemPost"),
            (105, "字典管理", 1, 6, 2, "dict", "system/dict/index", "system:dict:query", "dict", "SystemDictType"),
            (106, "租户管理", 1, 7, 2, "tenant", "system/tenant/index", "system:tenant:query", "list", "SystemTenant"),
            (107, "日志管理", 1, 8, 1, "log", None, "", "monitor", "SystemLog"),
            (500, "操作日志", 107, 1, 2, "operate-log", "system/operatelog/index", "system:operate-log:query", "form", "SystemOperateLog"),
            (501, "登录日志", 107, 2, 2, "login-log", "system/loginlog/index", "system:login-log:query", "logininfor", "SystemLoginLog"),
        ]
        for mid, name, pid, sort, mtype, path, comp, perm, icon, comp_name in menu_items:
            stmt = select(SystemMenu).where(SystemMenu.id == mid)
            item = (await session.execute(stmt)).scalar_one_or_none()
            if not item:
                session.add(SystemMenu(
                    id=mid, name=name, parent_id=pid, sort=sort, type=mtype,
                    path=path, component=comp, component_name=comp_name, permission=perm, icon=icon,
                    status=0, visible=True, creator="system", updater="system"
                ))
            else:
                item.parent_id = pid
                item.path = path
                item.component = comp
                item.component_name = comp_name


        await session.commit()
        print("Seed data idempotent check & sync completed.")

if __name__ == "__main__":
    asyncio.run(seed_data())
