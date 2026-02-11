from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.models.tenant import SystemTenant
from app.schemas.tenant import TenantPageReqVO, TenantSaveReqVO
from app.common.paging import PageResult
from app.core.security import hash_password

class TenantService:
    @staticmethod
    async def get_tenant_page(db: AsyncSession, req: TenantPageReqVO):
        stmt = select(SystemTenant).where(SystemTenant.deleted == 0)
        
        if req.name:
            stmt = stmt.where(SystemTenant.name.like(f"%{req.name}%"))
        if req.contact_name:
            stmt = stmt.where(SystemTenant.contact_name.like(f"%{req.contact_name}%"))
        if req.status is not None:
            stmt = stmt.where(SystemTenant.status == req.status)
            
        # 查询总数
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await db.scalar(count_stmt)
        
        # 分页
        stmt = stmt.order_by(SystemTenant.id.desc()).offset((req.page_no - 1) * req.page_size).limit(req.page_size)
        result = await db.execute(stmt)
        return PageResult(list=result.scalars().all(), total=total)

    @staticmethod
    async def get_tenant(db: AsyncSession, id: int):
        stmt = select(SystemTenant).where(SystemTenant.id == id, SystemTenant.deleted == 0)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def create_tenant(db: AsyncSession, req: TenantSaveReqVO):
        # 1. 校验租户名是否重复 (略)
        item = SystemTenant(
            **req.model_dump(exclude={"id", "username", "password"}),
            creator="admin",
            updater="admin"
        )
        db.add(item)
        await db.commit()
        await db.refresh(item)
        
        # 2. 如果传了用户名密码，应该创建对应的租户管理员 (暂时略过复杂逻辑，只创建租户)
        return item

    @staticmethod
    async def update_tenant(db: AsyncSession, req: TenantSaveReqVO):
        stmt = select(SystemTenant).where(SystemTenant.id == req.id, SystemTenant.deleted == 0)
        item = (await db.execute(stmt)).scalar_one_or_none()
        if not item:
            raise Exception("租户不存在")
            
        data = req.model_dump(exclude_unset=True, exclude={"id", "username", "password"})
        for key, value in data.items():
            setattr(item, key, value)
            
        item.updater = "admin"
        await db.commit()

    @staticmethod
    async def delete_tenant(db: AsyncSession, id: int):
        stmt = select(SystemTenant).where(SystemTenant.id == id)
        item = (await db.execute(stmt)).scalar_one_or_none()
        if item:
            item.deleted = 1
            await db.commit()

    @staticmethod
    async def export_tenants(db: AsyncSession, req: TenantPageReqVO):
        from app.utils.excel import ExcelUtils
        stmt = select(SystemTenant).where(SystemTenant.deleted == 0)
        
        if req.name:
            stmt = stmt.where(SystemTenant.name.like(f"%{req.name}%"))
        if req.contact_name:
            stmt = stmt.where(SystemTenant.contact_name.like(f"%{req.contact_name}%"))
        if req.status is not None:
            stmt = stmt.where(SystemTenant.status == req.status)
            
        result = await db.execute(stmt.order_by(SystemTenant.id.desc()))
        items = result.scalars().all()
        
        fields = {
            "id": "租户编号",
            "name": "租户名称",
            "package_id": "租户套餐",
            "contact_name": "联系人",
            "contact_mobile": "联系电话",
            "status": "租户状态",
            "create_time": "创建时间"
        }
        
        data = []
        for item in items:
            data.append({
                "id": item.id,
                "name": item.name,
                "package_id": item.package_id,
                "contact_name": item.contact_name,
                "contact_mobile": item.contact_mobile,
                "status": "开启" if item.status == 0 else "关闭",
                "create_time": item.create_time
            })
            
        return ExcelUtils.write(data, fields, "租户数据")
