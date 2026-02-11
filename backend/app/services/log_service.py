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

    @staticmethod
    async def export_login_logs(db: AsyncSession, req: LoginLogPageReqVO):
        from app.utils.excel import ExcelUtils
        stmt = select(SystemLoginLog).where(SystemLoginLog.deleted == 0)
        if req.username: stmt = stmt.where(SystemLoginLog.username.contains(req.username))
        if req.user_ip: stmt = stmt.where(SystemLoginLog.user_ip.contains(req.user_ip))
        if req.result is not None: stmt = stmt.where(SystemLoginLog.result == req.result)
        if req.create_time: stmt = stmt.where(SystemLoginLog.create_time.between(req.create_time[0], req.create_time[1]))
        
        result = await db.execute(stmt.order_by(desc(SystemLoginLog.id)))
        items = result.scalars().all()
        
        fields = {
            "id": "日志编号",
            "username": "用户账号",
            "user_ip": "登录地址",
            "user_agent": "浏览器",
            "result": "登录结果",
            "create_time": "登录时间"
        }
        
        data = []
        for item in items:
            data.append({
                "id": item.id,
                "username": item.username,
                "user_ip": item.user_ip,
                "user_agent": item.user_agent,
                "result": "成功" if item.result == 0 else "失败",
                "create_time": item.create_time
            })
            
        return ExcelUtils.write(data, fields, "登录日志")

    @staticmethod
    async def export_operate_logs(db: AsyncSession, req: OperateLogPageReqVO):
        from app.utils.excel import ExcelUtils
        from app.models.user import SystemUser
        stmt = select(SystemOperateLog, SystemUser.nickname.label("user_name")).outerjoin(
            SystemUser, SystemOperateLog.user_id == SystemUser.id
        ).where(SystemOperateLog.deleted == 0)
        
        if req.type: stmt = stmt.where(SystemOperateLog.type.contains(req.type))
        if req.user_id: stmt = stmt.where(SystemOperateLog.user_id == req.user_id)
        if req.success is not None: stmt = stmt.where(SystemOperateLog.success == req.success)
        if req.create_time: stmt = stmt.where(SystemOperateLog.create_time.between(req.create_time[0], req.create_time[1]))
        
        result = await db.execute(stmt.order_by(desc(SystemOperateLog.id)))
        rows = result.all()
        
        fields = {
            "id": "日志编号",
            "type": "操作模块",
            "sub_type": "操作内容",
            "user_name": "操作人员",
            "user_ip": "操作地址",
            "success": "执行状态",
            "create_time": "操作时间"
        }
        
        data = []
        for log, user_name in rows:
            data.append({
                "id": log.id,
                "type": log.type,
                "sub_type": log.sub_type,
                "user_name": user_name,
                "user_ip": log.user_ip,
                "success": "成功" if log.success else "失败",
                "create_time": log.create_time
            })
            
        return ExcelUtils.write(data, fields, "操作日志")

