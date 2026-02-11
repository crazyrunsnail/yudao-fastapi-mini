from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, update
from app.models.notify import SystemNotifyMessage, SystemNotifyTemplate
from app.schemas.notify import (
    NotifyMessagePageReqVO, NotifyMessageMyPageReqVO,
    NotifyTemplateCreateReqVO, NotifyTemplateUpdateReqVO, NotifyTemplatePageReqVO
)
from app.common.paging import PageResult
from datetime import datetime
import json

class NotifyService:
    @staticmethod
    async def get_my_page(db: AsyncSession, req: NotifyMessageMyPageReqVO, user_id: int):
        stmt = select(SystemNotifyMessage).where(SystemNotifyMessage.user_id == user_id, SystemNotifyMessage.deleted == 0)
        
        if req.read_status is not None:
            # 兼容 boolean 和 int
            stmt = stmt.where(SystemNotifyMessage.read_status == req.read_status)
        
        if req.create_time:
            stmt = stmt.where(SystemNotifyMessage.create_time.between(req.create_time[0], req.create_time[1]))
            
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await db.scalar(count_stmt)
        
        stmt = stmt.order_by(SystemNotifyMessage.create_time.desc()).offset((req.page_no - 1) * req.page_size).limit(req.page_size)
        result = await db.execute(stmt)
        rows = result.scalars().all()
        
        # 处理 params json
        items = []
        for row in rows:
            data = row.__dict__.copy()
            try:
                data['template_params'] = json.loads(row.template_params) if row.template_params else {}
            except:
                data['template_params'] = {}
            # 兼容 read_status 类型
            data['read_status'] = bool(row.read_status)
            items.append(data)
            
        return items, total

    @staticmethod
    async def get_unread_count(db: AsyncSession, user_id: int):
        stmt = select(func.count()).select_from(SystemNotifyMessage).where(
            SystemNotifyMessage.user_id == user_id, 
            SystemNotifyMessage.read_status == False,
            SystemNotifyMessage.deleted == 0
        )
        return await db.scalar(stmt)

    @staticmethod
    async def update_read(db: AsyncSession, ids: list[int], user_id: int):
        await db.execute(
            update(SystemNotifyMessage)
            .where(
                SystemNotifyMessage.id.in_(ids),
                SystemNotifyMessage.user_id == user_id,
                SystemNotifyMessage.read_status == False
            )
            .values(read_status=True, read_time=datetime.now())
        )
        await db.commit()
    
    @staticmethod
    async def update_all_read(db: AsyncSession, user_id: int):
        await db.execute(
            update(SystemNotifyMessage)
            .where(
                SystemNotifyMessage.user_id == user_id,
                SystemNotifyMessage.read_status == False
            )
            .values(read_status=True, read_time=datetime.now())
        )
        await db.commit()
    @staticmethod
    async def get_notify_message_page(db: AsyncSession, req: NotifyMessagePageReqVO):
        stmt = select(SystemNotifyMessage).where(SystemNotifyMessage.deleted == 0)
        
        if req.user_id:
            stmt = stmt.where(SystemNotifyMessage.user_id == req.user_id)
        if req.user_type:
             stmt = stmt.where(SystemNotifyMessage.user_type == req.user_type)
        if req.template_code:
            stmt = stmt.where(SystemNotifyMessage.template_code.like(f"%{req.template_code}%"))
        if req.template_type:
            stmt = stmt.where(SystemNotifyMessage.template_type == req.template_type)
        if req.create_time:
            stmt = stmt.where(SystemNotifyMessage.create_time.between(req.create_time[0], req.create_time[1]))
            
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await db.scalar(count_stmt)
        
        stmt = stmt.order_by(SystemNotifyMessage.create_time.desc()).offset((req.page_no - 1) * req.page_size).limit(req.page_size)
        result = await db.execute(stmt)
        rows = result.scalars().all()
        
        items = []
        for row in rows:
            data = row.__dict__.copy()
            try:
                data['template_params'] = json.loads(row.template_params) if row.template_params else {}
            except:
                data['template_params'] = {}
            data['read_status'] = bool(row.read_status)
            items.append(data)
            
        return items, total

    @staticmethod
    async def get_unread_list(db: AsyncSession, user_id: int, size: int = 10):
        stmt = select(SystemNotifyMessage).where(
            SystemNotifyMessage.user_id == user_id, 
            SystemNotifyMessage.read_status == False,
            SystemNotifyMessage.deleted == 0
        ).order_by(SystemNotifyMessage.create_time.desc()).limit(size)
        
        result = await db.execute(stmt)
        rows = result.scalars().all()
        
        items = []
        for row in rows:
            data = row.__dict__.copy()
            try:
                data['template_params'] = json.loads(row.template_params) if row.template_params else {}
            except:
                 data['template_params'] = {}
            data['read_status'] = bool(row.read_status)
            items.append(data)
            
        return items

    @staticmethod
    async def send_single_notify(db: AsyncSession, user_id: int, template_code: str, template_params: dict):
        # 1. 查询模板
        stmt = select(SystemNotifyTemplate).where(
            SystemNotifyTemplate.code == template_code,
            SystemNotifyTemplate.status == 0,
            SystemNotifyTemplate.deleted == 0
        )
        result = await db.execute(stmt)
        template = result.scalar_one_or_none()
        if not template:
            return None
        
        # 2. 渲染内容
        content = template.content
        if template_params:
            for key, value in template_params.items():
                content = content.replace(f"#{{{key}}}", str(value))
        
        # 3. 创建消息
        notify_message = SystemNotifyMessage(
            user_id=user_id,
            user_type=1, # 默认系统用户
            template_id=template.id,
            template_code=template.code,
            template_nickname=template.nickname,
            template_content=content,
            template_type=template.type,
            template_params=json.dumps(template_params, ensure_ascii=False),
            read_status=False
        )
        db.add(notify_message)
        await db.commit()
        await db.refresh(notify_message)
        return notify_message.id

class NotifyTemplateService:
    @staticmethod
    async def create_template(db: AsyncSession, req: NotifyTemplateCreateReqVO):
        template = SystemNotifyTemplate(**req.dict())
        if req.params:
            template.params = json.dumps(req.params, ensure_ascii=False)
        db.add(template)
        await db.commit()
        await db.refresh(template)
        return template.id

    @staticmethod
    async def update_template(db: AsyncSession, req: NotifyTemplateUpdateReqVO):
        update_data = req.dict(exclude_unset=True)
        if 'params' in update_data and update_data['params']:
            update_data['params'] = json.dumps(update_data['params'], ensure_ascii=False)
        
        await db.execute(
            update(SystemNotifyTemplate)
            .where(SystemNotifyTemplate.id == req.id)
            .values(**update_data)
        )
        await db.commit()

    @staticmethod
    async def delete_template(db: AsyncSession, id: int):
        await db.execute(
            update(SystemNotifyTemplate)
            .where(SystemNotifyTemplate.id == id)
            .values(deleted=1)
        )
        await db.commit()

    @staticmethod
    async def get_template(db: AsyncSession, id: int):
        stmt = select(SystemNotifyTemplate).where(SystemNotifyTemplate.id == id, SystemNotifyTemplate.deleted == 0)
        result = await db.execute(stmt)
        row = result.scalar_one_or_none()
        if row:
            data = row.__dict__.copy()
            data['params'] = json.loads(row.params) if row.params else []
            return data
        return None

    @staticmethod
    async def get_template_page(db: AsyncSession, req: NotifyTemplatePageReqVO):
        stmt = select(SystemNotifyTemplate).where(SystemNotifyTemplate.deleted == 0)
        
        if req.name:
            stmt = stmt.where(SystemNotifyTemplate.name.like(f"%{req.name}%"))
        if req.code:
            stmt = stmt.where(SystemNotifyTemplate.code.like(f"%{req.code}%"))
        if req.status is not None:
             stmt = stmt.where(SystemNotifyTemplate.status == req.status)
        if req.create_time:
            stmt = stmt.where(SystemNotifyTemplate.create_time.between(req.create_time[0], req.create_time[1]))
            
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await db.scalar(count_stmt)
        
        stmt = stmt.order_by(SystemNotifyTemplate.create_time.desc()).offset((req.page_no - 1) * req.page_size).limit(req.page_size)
        result = await db.execute(stmt)
        rows = result.scalars().all()
        
        items = []
        for row in rows:
            data = row.__dict__.copy()
            data['params'] = json.loads(row.params) if row.params else []
            items.append(data)
            
        return items, total
