from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.login_log import SystemLoginLog
from app.models.operate_log import SystemOperateLog
from app.schemas.log import LoginLogPageReqVO, OperateLogPageReqVO
from typing import List

class LogService:
    @staticmethod
    async def get_login_log_page(db: AsyncSession, req: LoginLogPageReqVO):
        stmt = select(SystemLoginLog).where(SystemLoginLog.deleted == 0)
        if req.username:
            stmt = stmt.where(SystemLoginLog.username.contains(req.username))
        if req.user_ip:
            stmt = stmt.where(SystemLoginLog.user_ip.contains(req.user_ip))
        if req.result is not None:
            stmt = stmt.where(SystemLoginLog.result == req.result)
        if req.create_time:
            stmt = stmt.where(SystemLoginLog.create_time.between(req.create_time[0], req.create_time[1]))
            
        stmt = stmt.order_by(desc(SystemLoginLog.id))
        return await LogService._get_page(db, stmt, req.page_no, req.page_size)

    @staticmethod
    async def get_operate_log_page(db: AsyncSession, req: OperateLogPageReqVO):
        from app.models.user import SystemUser
        stmt = select(SystemOperateLog, SystemUser.nickname.label("user_name")).outerjoin(
            SystemUser, SystemOperateLog.user_id == SystemUser.id
        ).where(SystemOperateLog.deleted == 0)
        
        if req.type:
            stmt = stmt.where(SystemOperateLog.type.contains(req.type))
        if req.user_id:
            stmt = stmt.where(SystemOperateLog.user_id == req.user_id)
        if req.success is not None:
            stmt = stmt.where(SystemOperateLog.success == req.success)
        if req.create_time:
            stmt = stmt.where(SystemOperateLog.create_time.between(req.create_time[0], req.create_time[1]))
            
        stmt = stmt.order_by(desc(SystemOperateLog.id))
        
        # Count total
        from sqlalchemy import func
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await db.execute(count_stmt)).scalar() or 0
        
        # Get items
        result = await db.execute(stmt.offset((req.page_no - 1) * req.page_size).limit(req.page_size))
        rows = result.all()
        
        items = []
        for log, user_name in rows:
            # Manually map to Pydantic-friendly dict or object
            log_dict = {c.name: getattr(log, c.name) for c in log.__table__.columns}
            log_dict["user_name"] = user_name
            items.append(log_dict)
            
        return items, total

    @staticmethod
    async def _get_page(db: AsyncSession, stmt, page_no: int, page_size: int):
        from sqlalchemy import func
        # Count total
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await db.execute(count_stmt)).scalar() or 0
        
        # Get items
        result = await db.execute(stmt.offset((page_no - 1) * page_size).limit(page_size))
        items = result.scalars().all()
        
        return items, total

    @staticmethod
    async def create_login_log(db: AsyncSession, log_data: dict):
        log = SystemLoginLog(**log_data, creator="system", updater="system", tenant_id=0)
        db.add(log)
        await db.commit()

    @staticmethod
    async def create_operate_log(db: AsyncSession, log_data: dict):
        log = SystemOperateLog(**log_data, creator="system", updater="system", tenant_id=0)
        db.add(log)
        await db.commit()

