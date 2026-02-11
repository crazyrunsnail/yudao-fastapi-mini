from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, desc
from app.models.dict import SystemDictType, SystemDictData
from app.schemas.dict import (
    DictTypePageReqVO, DictTypeSaveReqVO,
    DictDataPageReqVO, DictDataSaveReqVO
)
from typing import List

class DictTypeService:
    @staticmethod
    async def get_dict_type_page(db: AsyncSession, req: DictTypePageReqVO):
        stmt = select(SystemDictType).where(SystemDictType.deleted == 0)
        
        if req.name:
            stmt = stmt.where(SystemDictType.name.like(f"%{req.name}%"))
        if req.type:
            stmt = stmt.where(SystemDictType.type.like(f"%{req.type}%"))
        if req.status is not None:
            stmt = stmt.where(SystemDictType.status == req.status)
        if req.create_time:
             stmt = stmt.where(SystemDictType.create_time.between(req.create_time[0], req.create_time[1]))

        # 查询总数
        from sqlalchemy import func
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await db.scalar(count_stmt)

        # 分页
        stmt = stmt.order_by(desc(SystemDictType.id)).offset((req.page_no - 1) * req.page_size).limit(req.page_size)
        result = await db.execute(stmt)
        items = result.scalars().all()
        
        return items, total

    @staticmethod
    async def get_dict_type(db: AsyncSession, id: int):
        return await db.get(SystemDictType, id)

    @staticmethod
    async def create_dict_type(db: AsyncSession, req: DictTypeSaveReqVO):
        db_type = SystemDictType(**req.model_dump(exclude={"id"}), creator="admin", updater="admin")
        db.add(db_type)
        await db.commit()
        await db.refresh(db_type)
        return db_type

    @staticmethod
    async def update_dict_type(db: AsyncSession, req: DictTypeSaveReqVO):
        await db.execute(
            update(SystemDictType)
            .where(SystemDictType.id == req.id)
            .values(**req.model_dump(exclude={"id"}), updater="admin")
        )
        await db.commit()

    @staticmethod
    async def delete_dict_type(db: AsyncSession, id: int):
        await db.execute(update(SystemDictType).where(SystemDictType.id == id).values(deleted=1))
        await db.commit()

    @staticmethod
    async def get_all_dict_types(db: AsyncSession):
        result = await db.execute(select(SystemDictType).where(SystemDictType.deleted == 0))
        return result.scalars().all()

    @staticmethod
    async def export_dict_types(db: AsyncSession, req: DictTypePageReqVO):
        from app.utils.excel import ExcelUtils
        stmt = select(SystemDictType).where(SystemDictType.deleted == 0)
        if req.name: stmt = stmt.where(SystemDictType.name.like(f"%{req.name}%"))
        if req.type: stmt = stmt.where(SystemDictType.type.like(f"%{req.type}%"))
        if req.status is not None: stmt = stmt.where(SystemDictType.status == req.status)
        
        result = await db.execute(stmt.order_by(desc(SystemDictType.id)))
        items = result.scalars().all()
        
        fields = {
            "name": "字典名称",
            "type": "字典类型",
            "status": "状态",
            "remark": "备注",
            "create_time": "创建时间"
        }
        
        data = []
        for item in items:
            data.append({
                "name": item.name,
                "type": item.type,
                "status": "开启" if item.status == 0 else "关闭",
                "remark": item.remark,
                "create_time": item.create_time
            })
            
        return ExcelUtils.write(data, fields, "字典类型")

class DictDataService:
    @staticmethod
    async def get_dict_data_page(db: AsyncSession, req: DictDataPageReqVO):
        stmt = select(SystemDictData).where(SystemDictData.deleted == 0)
        if req.label:
            stmt = stmt.where(SystemDictData.label.contains(req.label))
        if req.dict_type:
            stmt = stmt.where(SystemDictData.dict_type == req.dict_type)
        if req.status is not None:
            stmt = stmt.where(SystemDictData.status == req.status)
            
        total_stmt = select(SystemDictData).where(SystemDictData.deleted == 0)
        if req.label: total_stmt = total_stmt.where(SystemDictData.label.contains(req.label))
        if req.dict_type: total_stmt = total_stmt.where(SystemDictData.dict_type == req.dict_type)
        if req.status is not None: total_stmt = total_stmt.where(SystemDictData.status == req.status)

        result = await db.execute(stmt.order_by(SystemDictData.sort).offset((req.page_no - 1) * req.page_size).limit(req.page_size))
        items = result.scalars().all()
        
        from sqlalchemy import func
        total_result = await db.execute(select(func.count()).select_from(total_stmt.subquery()))
        total = total_result.scalar()
        
        return items, total

    @staticmethod
    async def get_dict_data(db: AsyncSession, id: int):
        return await db.get(SystemDictData, id)

    @staticmethod
    async def create_dict_data(db: AsyncSession, req: DictDataSaveReqVO):
        db_data = SystemDictData(**req.model_dump(exclude={"id"}), creator="admin", updater="admin")
        db.add(db_data)
        await db.commit()
        await db.refresh(db_data)
        return db_data

    @staticmethod
    async def update_dict_data(db: AsyncSession, req: DictDataSaveReqVO):
        await db.execute(
            update(SystemDictData)
            .where(SystemDictData.id == req.id)
            .values(**req.model_dump(exclude={"id"}), updater="admin")
        )
        await db.commit()

    @staticmethod
    async def delete_dict_data(db: AsyncSession, id: int):
        await db.execute(update(SystemDictData).where(SystemDictData.id == id).values(deleted=1))
        await db.commit()

    @staticmethod
    async def get_simple_dict_data(db: AsyncSession):
        result = await db.execute(select(SystemDictData).where(SystemDictData.deleted == 0, SystemDictData.status == 0).order_by(SystemDictData.sort))
        return result.scalars().all()

    @staticmethod
    async def export_dict_data(db: AsyncSession, req: DictDataPageReqVO):
        from app.utils.excel import ExcelUtils
        stmt = select(SystemDictData).where(SystemDictData.deleted == 0)
        if req.label: stmt = stmt.where(SystemDictData.label.contains(req.label))
        if req.dict_type: stmt = stmt.where(SystemDictData.dict_type == req.dict_type)
        if req.status is not None: stmt = stmt.where(SystemDictData.status == req.status)
        
        result = await db.execute(stmt.order_by(SystemDictData.sort))
        items = result.scalars().all()
        
        fields = {
            "dict_type": "字典类型",
            "label": "字典标签",
            "value": "字典键值",
            "sort": "字典排序",
            "status": "状态",
            "remark": "备注",
            "create_time": "创建时间"
        }
        
        data = []
        for item in items:
            data.append({
                "dict_type": item.dict_type,
                "label": item.label,
                "value": item.value,
                "sort": item.sort,
                "status": "开启" if item.status == 0 else "关闭",
                "remark": item.remark,
                "create_time": item.create_time
            })
            
        return ExcelUtils.write(data, fields, "字典数据")
