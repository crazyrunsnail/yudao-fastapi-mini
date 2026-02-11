from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, update
from app.models.tenant import SystemTenantPackage
from app.schemas.tenant_package import TenantPackagePageReqVO, TenantPackageSaveReqVO, TenantPackageSimpleRespVO
from app.common.paging import PageResult
from typing import List

class TenantPackageService:
    @staticmethod
    async def get_tenant_package_page(db: AsyncSession, req: TenantPackagePageReqVO):
        stmt = select(SystemTenantPackage).where(SystemTenantPackage.deleted == 0)
        
        if req.name:
            stmt = stmt.where(SystemTenantPackage.name.like(f"%{req.name}%"))
        if req.status is not None:
            stmt = stmt.where(SystemTenantPackage.status == req.status)
            
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await db.scalar(count_stmt)
        
        stmt = stmt.order_by(SystemTenantPackage.id.desc()).offset((req.page_no - 1) * req.page_size).limit(req.page_size)
        result = await db.execute(stmt)
        
        rows = result.scalars().all()
        # 处理 menu_ids 字符串转列表
        items = []
        for row in rows:
            menu_ids_list = [int(mid) for mid in row.menu_ids.split(",")] if row.menu_ids else []
            item_dict = row.__dict__.copy()
            item_dict['menu_ids'] = menu_ids_list
            items.append(item_dict)
            
        return PageResult(list=items, total=total)

    @staticmethod
    async def get_tenant_package(db: AsyncSession, id: int):
        stmt = select(SystemTenantPackage).where(SystemTenantPackage.id == id, SystemTenantPackage.deleted == 0)
        item = (await db.execute(stmt)).scalar_one_or_none()
        if not item:
            return None
        
        item_dict = item.__dict__.copy()
        item_dict['menu_ids'] = [int(mid) for mid in item.menu_ids.split(",")] if item.menu_ids else []
        return item_dict

    @staticmethod
    async def create_tenant_package(db: AsyncSession, req: TenantPackageSaveReqVO):
        menu_ids_str = ",".join(map(str, req.menu_ids)) if req.menu_ids else ""
        item = SystemTenantPackage(
            **req.model_dump(exclude={"id", "menu_ids"}),
            menu_ids=menu_ids_str,
            creator="admin",
            updater="admin"
        )
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item

    @staticmethod
    async def update_tenant_package(db: AsyncSession, req: TenantPackageSaveReqVO):
        stmt = select(SystemTenantPackage).where(SystemTenantPackage.id == req.id, SystemTenantPackage.deleted == 0)
        item = (await db.execute(stmt)).scalar_one_or_none()
        if not item:
            raise Exception("套餐不存在")
            
        data = req.model_dump(exclude_unset=True, exclude={"id", "menu_ids"})
        for key, value in data.items():
            setattr(item, key, value)
            
        if req.menu_ids is not None:
            item.menu_ids = ",".join(map(str, req.menu_ids))
            
        item.updater = "admin"
        await db.commit()

    @staticmethod
    async def delete_tenant_package(db: AsyncSession, id: int):
        stmt = select(SystemTenantPackage).where(SystemTenantPackage.id == id)
        item = (await db.execute(stmt)).scalar_one_or_none()
        if item:
            item.deleted = 1
            await db.commit()

    @staticmethod
    async def get_tenant_package_simple_list(db: AsyncSession):
        stmt = select(SystemTenantPackage).where(SystemTenantPackage.status == 0, SystemTenantPackage.deleted == 0)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def export_tenant_packages(db: AsyncSession, req: TenantPackagePageReqVO):
        from app.utils.excel import ExcelUtils
        stmt = select(SystemTenantPackage).where(SystemTenantPackage.deleted == 0)
        
        if req.name:
            stmt = stmt.where(SystemTenantPackage.name.like(f"%{req.name}%"))
        if req.status is not None:
            stmt = stmt.where(SystemTenantPackage.status == req.status)
            
        result = await db.execute(stmt.order_by(SystemTenantPackage.id.desc()))
        items = result.scalars().all()
        
        fields = {
            "id": "套餐编号",
            "name": "套餐名称",
            "status": "状态",
            "remark": "备注",
            "create_time": "创建时间"
        }
        
        data = []
        for item in items:
            data.append({
                "id": item.id,
                "name": item.name,
                "status": "开启" if item.status == 0 else "关闭",
                "remark": item.remark,
                "create_time": item.create_time
            })
            
        return ExcelUtils.write(data, fields, "租户套餐数据")
