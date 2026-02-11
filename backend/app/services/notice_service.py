from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, update
from app.models.notice import SystemNotice
from app.schemas.notice import NoticeCreateReqVO, NoticeUpdateReqVO, NoticePageReqVO
from app.common.paging import PageResult
from typing import List

class NoticeService:
    @staticmethod
    async def create_notice(db: AsyncSession, req: NoticeCreateReqVO) -> int:
        notice = SystemNotice(**req.dict())
        db.add(notice)
        await db.commit()
        await db.refresh(notice)
        return notice.id

    @staticmethod
    async def update_notice(db: AsyncSession, req: NoticeUpdateReqVO):
        await db.execute(
            update(SystemNotice)
            .where(SystemNotice.id == req.id)
            .values(**req.dict(exclude_unset=True))
        )
        await db.commit()

    @staticmethod
    async def delete_notice(db: AsyncSession, id: int):
        await db.execute(
            update(SystemNotice)
            .where(SystemNotice.id == id)
            .values(deleted=1)
        )
        await db.commit()

    @staticmethod
    async def get_notice(db: AsyncSession, id: int):
        stmt = select(SystemNotice).where(SystemNotice.id == id, SystemNotice.deleted == 0)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_notice_page(db: AsyncSession, req: NoticePageReqVO):
        stmt = select(SystemNotice).where(SystemNotice.deleted == 0)
        
        if req.title:
            stmt = stmt.where(SystemNotice.title.like(f"%{req.title}%"))
        if req.status is not None:
            stmt = stmt.where(SystemNotice.status == req.status)
            
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await db.scalar(count_stmt)
        
        stmt = stmt.order_by(SystemNotice.id.desc()).offset((req.page_no - 1) * req.page_size).limit(req.page_size)
        result = await db.execute(stmt)
        rows = result.scalars().all()
        
        return rows, total
