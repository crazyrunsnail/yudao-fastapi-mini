from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete
from app.models.user_role import SystemUserRole
from app.models.role_menu import SystemRoleMenu
from typing import Set

class PermissionService:
    @staticmethod
    async def get_user_role_ids(db: AsyncSession, user_id: int):
        stmt = select(SystemUserRole.role_id).where(SystemUserRole.user_id == user_id, SystemUserRole.deleted == 0)
        result = await db.execute(stmt)
        return set(result.scalars().all())

    @staticmethod
    async def assign_user_role(db: AsyncSession, user_id: int, role_ids: Set[int]):
        # 1. 获取现有角色
        current_role_ids = await PermissionService.get_user_role_ids(db, user_id)
        
        # 2. 计算需要添加和删除的角色
        roles_to_add = role_ids - current_role_ids
        roles_to_delete = current_role_ids - role_ids
        
        # 3. 删除不再需要的角色
        if roles_to_delete:
            delete_stmt = delete(SystemUserRole).where(
                SystemUserRole.user_id == user_id,
                SystemUserRole.role_id.in_(roles_to_delete)
            )
            await db.execute(delete_stmt)
            
        # 4. 插入新角色
        if roles_to_add:
            for rid in roles_to_add:
                db.add(SystemUserRole(user_id=user_id, role_id=rid, creator="admin", updater="admin", tenant_id=0))
                
        await db.commit()

    @staticmethod
    async def get_role_menu_ids(db: AsyncSession, role_id: int):
        stmt = select(SystemRoleMenu.menu_id).where(SystemRoleMenu.role_id == role_id, SystemRoleMenu.deleted == 0)
        result = await db.execute(stmt)
        return set(result.scalars().all())

    @staticmethod
    async def get_role_menu_ids_by_role_ids(db: AsyncSession, role_ids: Set[int]):
        stmt = select(SystemRoleMenu.menu_id).where(SystemRoleMenu.role_id.in_(role_ids), SystemRoleMenu.deleted == 0)
        result = await db.execute(stmt)
        return set(result.scalars().all())

    @staticmethod
    async def assign_role_menu(db: AsyncSession, role_id: int, menu_ids: Set[int]):
        # 1. 获取现有菜单
        current_menu_ids = await PermissionService.get_role_menu_ids(db, role_id)
        
        # 2. 计算需要添加和删除的菜单
        menus_to_add = menu_ids - current_menu_ids
        menus_to_delete = current_menu_ids - menu_ids
        
        # 3. 删除不再需要的菜单
        if menus_to_delete:
            delete_stmt = delete(SystemRoleMenu).where(
                SystemRoleMenu.role_id == role_id,
                SystemRoleMenu.menu_id.in_(menus_to_delete)
            )
            await db.execute(delete_stmt)
            
        # 4. 插入新菜单
        if menus_to_add:
            for mid in menus_to_add:
                db.add(SystemRoleMenu(role_id=role_id, menu_id=mid, creator="admin", updater="admin", tenant_id=0))
                
        await db.commit()
    @staticmethod
    async def get_user_permissions(db: AsyncSession, user_id: int):
        from app.models.menu import SystemMenu
        from app.models.role import SystemRole
        
        # 1. 获取用户角色
        role_ids = await PermissionService.get_user_role_ids(db, user_id)
        if not role_ids:
            return set()
            
        # 2. 获取启用状态的角色对应的菜单 ID
        stmt = select(SystemRoleMenu.menu_id).join(
            SystemRole, and_(SystemRole.id == SystemRoleMenu.role_id, SystemRole.status == 0, SystemRole.deleted == 0)
        ).where(SystemRoleMenu.role_id.in_(role_ids), SystemRoleMenu.deleted == 0)
        result = await db.execute(stmt)
        menu_ids = set(result.scalars().all())
        
        if not menu_ids:
            return set()
            
        # 3. 获取菜单对应的权限标识
        stmt = select(SystemMenu.permission).where(
            SystemMenu.id.in_(menu_ids),
            SystemMenu.deleted == 0,
            SystemMenu.status == 0,
            SystemMenu.permission != ""
        )
        result = await db.execute(stmt)
        return set(result.scalars().all())
