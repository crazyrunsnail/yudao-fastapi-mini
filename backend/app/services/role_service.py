from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.role import SystemRole
from app.schemas.role import RolePageReqVO, RoleSaveReqVO
from app.common.paging import PageResult

class RoleService:
    @staticmethod
    async def get_role_page(db: AsyncSession, req: RolePageReqVO):
        stmt = select(SystemRole).where(SystemRole.deleted == 0)
        
        if req.name:
            stmt = stmt.where(SystemRole.name.like(f"%{req.name}%"))
        if req.code:
            stmt = stmt.where(SystemRole.code.like(f"%{req.code}%"))
        if req.status is not None:
            stmt = stmt.where(SystemRole.status == req.status)
            
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await db.scalar(count_stmt)
        
        stmt = stmt.order_by(SystemRole.id.desc()).offset((req.page_no - 1) * req.page_size).limit(req.page_size)
        result = await db.execute(stmt)
        roles = result.scalars().all()
        
        return PageResult(list=roles, total=total)

    @staticmethod
    async def create_role(db: AsyncSession, req: RoleSaveReqVO):
        role = SystemRole(
            **req.model_dump(exclude={"id"}),
            tenant_id=0,
            creator="admin",
            updater="admin"
        )
        db.add(role)
        await db.commit()
        await db.refresh(role)
        return role.id

    @staticmethod
    async def update_role(db: AsyncSession, req: RoleSaveReqVO):
        stmt = select(SystemRole).where(SystemRole.id == req.id, SystemRole.deleted == 0)
        role = (await db.execute(stmt)).scalar_one_or_none()
        if not role:
            raise Exception("角色不存在")
            
        data = req.model_dump(exclude_unset=True, exclude={"id"})
        for key, value in data.items():
            setattr(role, key, value)
            
        role.updater = "admin"
        await db.commit()

    @staticmethod
    async def delete_role(db: AsyncSession, id: int):
        stmt = select(SystemRole).where(SystemRole.id == id)
        role = (await db.execute(stmt)).scalar_one_or_none()
        if role:
            role.deleted = 1
            await db.commit()

    @staticmethod
    async def get_role(db: AsyncSession, id: int):
        stmt = select(SystemRole).where(SystemRole.id == id, SystemRole.deleted == 0)
        return (await db.execute(stmt)).scalar_one_or_none()
        
    @staticmethod
    async def get_role_list_by_status(db: AsyncSession, status: int):
        stmt = select(SystemRole).where(SystemRole.status == status, SystemRole.deleted == 0)
        result = await db.execute(stmt)
        return result.scalars().all()
