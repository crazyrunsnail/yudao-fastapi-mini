from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.menu import SystemMenu
from app.schemas.menu import MenuSaveReqVO, MenuSimpleRespVO
from typing import List

class MenuService:
    @staticmethod
    async def get_all_menus(db: AsyncSession):
        stmt = select(SystemMenu).where(SystemMenu.deleted == 0).order_by(SystemMenu.parent_id, SystemMenu.sort)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_menu_list(db: AsyncSession, name=None, status=None):
        stmt = select(SystemMenu).where(SystemMenu.deleted == 0)
        if name:
            stmt = stmt.where(SystemMenu.name.like(f"%{name}%"))
        if status is not None:
            stmt = stmt.where(SystemMenu.status == status)
        stmt = stmt.order_by(SystemMenu.parent_id, SystemMenu.sort)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_menu_list_by_ids(db: AsyncSession, menu_ids: List[int]):
        stmt = select(SystemMenu).where(SystemMenu.id.in_(menu_ids), SystemMenu.deleted == 0).order_by(SystemMenu.sort)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def create_menu(db: AsyncSession, req: MenuSaveReqVO):
        menu = SystemMenu(
            **req.model_dump(exclude={"id"}),
            creator="admin",
            updater="admin"
        )
        db.add(menu)
        await db.commit()
        await db.refresh(menu)
        return menu.id

    @staticmethod
    async def update_menu(db: AsyncSession, req: MenuSaveReqVO):
        stmt = select(SystemMenu).where(SystemMenu.id == req.id, SystemMenu.deleted == 0)
        menu = (await db.execute(stmt)).scalar_one_or_none()
        if not menu:
            raise Exception("菜单不存在")
            
        data = req.model_dump(exclude_unset=True, exclude={"id"})
        for key, value in data.items():
            setattr(menu, key, value)
            
        menu.updater = "admin"
        await db.commit()

    @staticmethod
    async def delete_menu(db: AsyncSession, id: int):
        # 检查是否有子菜单
        child_stmt = select(SystemMenu).where(SystemMenu.parent_id == id, SystemMenu.deleted == 0)
        child = (await db.execute(child_stmt)).scalar_one_or_none()
        if child:
            raise Exception("存在子菜单，无法删除")
            
        stmt = select(SystemMenu).where(SystemMenu.id == id)
        menu = (await db.execute(stmt)).scalar_one_or_none()
        if menu:
            menu.deleted = 1
            await db.commit()

    @staticmethod
    async def get_menu(db: AsyncSession, id: int):
        stmt = select(SystemMenu).where(SystemMenu.id == id, SystemMenu.deleted == 0)
        return (await db.execute(stmt)).scalar_one_or_none()

    @staticmethod
    async def build_menu_tree(menus: List[SystemMenu]):
        from app.schemas.menu import MenuRespVO
        # 1. 转换为 VO 列表
        all_nodes = []
        for menu in menus:
            node = MenuRespVO(
                id=menu.id,
                name=menu.name,
                permission=menu.permission,
                type=menu.type,
                sort=menu.sort,
                parent_id=menu.parent_id,
                path=menu.path,
                icon=menu.icon,
                component=menu.component,
                component_name=menu.component_name,
                status=menu.status,
                visible=menu.visible,
                keep_alive=menu.keep_alive,
                always_show=menu.always_show,
                create_time=menu.create_time,
                children=None
            )
            all_nodes.append(node)
            
        # 2. 构建树形结构
        node_map = {node.id: node for node in all_nodes}
        tree = []
        for node in all_nodes:
            if node.parent_id == 0:
                tree.append(node)
            else:
                parent = node_map.get(node.parent_id)
                if parent:
                    if parent.children is None:
                        parent.children = []
                    parent.children.append(node)
        return tree
