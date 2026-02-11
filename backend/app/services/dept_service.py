from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_
from app.models.dept import SystemDept
from app.schemas.dept import DeptListReqVO, DeptSaveReqVO
from typing import List

class DeptService:
    @staticmethod
    async def get_dept_list(db: AsyncSession, req: DeptListReqVO):
        stmt = select(SystemDept).where(SystemDept.deleted == 0)
        if req.name:
            stmt = stmt.where(SystemDept.name.contains(req.name))
        if req.status is not None:
            stmt = stmt.where(SystemDept.status == req.status)
        
        result = await db.execute(stmt.order_by(SystemDept.sort))
        return result.scalars().all()

    @staticmethod
    async def get_dept(db: AsyncSession, id: int):
        return await db.get(SystemDept, id)

    @staticmethod
    async def create_dept(db: AsyncSession, req: DeptSaveReqVO):
        db_dept = SystemDept(**req.model_dump(exclude={"id"}), creator="admin", updater="admin", tenant_id=0)
        db.add(db_dept)
        await db.commit()
        await db.refresh(db_dept)
        return db_dept

    @staticmethod
    async def update_dept(db: AsyncSession, req: DeptSaveReqVO):
        await db.execute(
            update(SystemDept)
            .where(SystemDept.id == req.id)
            .values(**req.model_dump(exclude={"id"}), updater="admin")
        )
        await db.commit()

    @staticmethod
    async def delete_dept(db: AsyncSession, id: int):
        await db.execute(update(SystemDept).where(SystemDept.id == id).values(deleted=1))
        await db.commit()

    @staticmethod
    async def get_dept_simple_list(db: AsyncSession):
        stmt = select(SystemDept).where(SystemDept.status == 0, SystemDept.deleted == 0)
        result = await db.execute(stmt)
        return result.scalars().all()
