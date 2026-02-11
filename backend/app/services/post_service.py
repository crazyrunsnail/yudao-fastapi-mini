from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, desc
from app.models.post import SystemPost
from app.schemas.post import PostPageReqVO, PostSaveReqVO
from typing import List

class PostService:
    @staticmethod
    async def get_post_page(db: AsyncSession, req: PostPageReqVO):
        stmt = select(SystemPost).where(SystemPost.deleted == 0)
        if req.name:
            stmt = stmt.where(SystemPost.name.contains(req.name))
        if req.code:
            stmt = stmt.where(SystemPost.code.contains(req.code))
        if req.status is not None:
            stmt = stmt.where(SystemPost.status == req.status)
        
        # Total
        from sqlalchemy import func
        total_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await db.execute(total_stmt)).scalar()

        result = await db.execute(stmt.order_by(SystemPost.sort).offset((req.page_no - 1) * req.page_size).limit(req.page_size))
        items = result.scalars().all()
        
        return items, total

    @staticmethod
    async def get_post(db: AsyncSession, id: int):
        return await db.get(SystemPost, id)

    @staticmethod
    async def create_post(db: AsyncSession, req: PostSaveReqVO):
        db_post = SystemPost(**req.model_dump(exclude={"id"}), creator="admin", updater="admin", tenant_id=0)
        db.add(db_post)
        await db.commit()
        await db.refresh(db_post)
        return db_post

    @staticmethod
    async def update_post(db: AsyncSession, req: PostSaveReqVO):
        await db.execute(
            update(SystemPost)
            .where(SystemPost.id == req.id)
            .values(**req.model_dump(exclude={"id"}), updater="admin")
        )
        await db.commit()

    @staticmethod
    async def delete_post(db: AsyncSession, id: int):
        await db.execute(update(SystemPost).where(SystemPost.id == id).values(deleted=1))
        await db.commit()

    @staticmethod
    async def get_post_simple_list(db: AsyncSession):
        stmt = select(SystemPost).where(SystemPost.status == 0, SystemPost.deleted == 0)
        result = await db.execute(stmt)
        return result.scalars().all()
