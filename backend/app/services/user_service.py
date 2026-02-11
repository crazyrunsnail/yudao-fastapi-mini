from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, delete
from app.models.user import SystemUser
from app.schemas.user import UserPageReqVO, UserSaveReqVO, UserProfileUpdateReqVO, UserProfileUpdatePasswordReqVO
from app.core.security import hash_password
from app.common.paging import PageResult
import json

class UserService:
    @staticmethod
    async def get_user_page(db: AsyncSession, req: UserPageReqVO):
        from app.models.dept import SystemDept
        # 1. 构造查询条件
        # 使用 select(SystemUser, SystemDept.name) 来获取部门名称
        stmt = select(SystemUser, SystemDept.name.label("dept_name")).outerjoin(
            SystemDept, and_(SystemUser.dept_id == SystemDept.id, SystemDept.deleted == 0)
        ).where(SystemUser.deleted == 0)
        
        if req.username:
            stmt = stmt.where(SystemUser.username.like(f"%{req.username}%"))
        if req.mobile:
            stmt = stmt.where(SystemUser.mobile.like(f"%{req.mobile}%"))
        if req.status is not None:
            stmt = stmt.where(SystemUser.status == req.status)
        if req.dept_id:
            stmt = stmt.where(SystemUser.dept_id == req.dept_id)
            
        # 2. 查询总数
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await db.scalar(count_stmt)
        
        # 3. 分页查询
        stmt = stmt.order_by(SystemUser.id.desc()).offset((req.page_no - 1) * req.page_size).limit(req.page_size)
        result = await db.execute(stmt)
        rows = result.all()
        
        user_list = []
        for row in rows:
            user = row[0]
            dept_name = row[1]
            # 转换为 dict 以便 Pydantic 处理，或者手动赋值
            user_data = user.__dict__.copy()
            user_data["dept_name"] = dept_name
            if user.post_ids:
                try:
                    user_data["post_ids"] = json.loads(user.post_ids)
                except:
                    user_data["post_ids"] = []
            else:
                user_data["post_ids"] = []
            user_list.append(user_data)
        
        return PageResult(list=user_list, total=total)

    @staticmethod
    async def create_user(db: AsyncSession, req: UserSaveReqVO):
        # 转换 post_ids 为字符串
        post_ids_str = json.dumps(req.post_ids) if req.post_ids else "[]"
        
        user = SystemUser(
            **req.model_dump(exclude={"post_ids", "id", "password"}),
            password=hash_password(req.password) if req.password else "",
            post_ids=post_ids_str,
            tenant_id=0,
            creator="admin",
            updater="admin"
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user.id

    @staticmethod
    async def update_user(db: AsyncSession, req: UserSaveReqVO):
        stmt = select(SystemUser).where(SystemUser.id == req.id, SystemUser.deleted == 0)
        user = (await db.execute(stmt)).scalar_one_or_none()
        if not user:
            raise Exception("用户不存在")
            
        # 更新字段
        data = req.model_dump(exclude_unset=True, exclude={"id", "post_ids", "password"})
        for key, value in data.items():
            setattr(user, key, value)
            
        if req.post_ids is not None:
            user.post_ids = json.dumps(req.post_ids)
            
        if req.password:
            user.password = hash_password(req.password)
            
        user.updater = "admin"
        await db.commit()

    @staticmethod
    async def delete_user(db: AsyncSession, id: int):
        stmt = select(SystemUser).where(SystemUser.id == id)
        user = (await db.execute(stmt)).scalar_one_or_none()
        if user:
            user.deleted = 1
            await db.commit()

    @staticmethod
    async def get_user(db: AsyncSession, id: int):
        from app.models.dept import SystemDept
        stmt = select(SystemUser, SystemDept.name.label("dept_name")).outerjoin(
            SystemDept, and_(SystemUser.dept_id == SystemDept.id, SystemDept.deleted == 0)
        ).where(SystemUser.id == id, SystemUser.deleted == 0)
        
        result = await db.execute(stmt)
        row = result.one_or_none()
        if not row:
            return None
            
        user = row[0]
        dept_name = row[1]
        user_data = user.__dict__.copy()
        user_data["dept_name"] = dept_name
        if user.post_ids:
            try:
                user_data["post_ids"] = json.loads(user.post_ids)
            except:
                user_data["post_ids"] = []
        else:
            user_data["post_ids"] = []
        return user_data

    @staticmethod
    async def update_user_password(db: AsyncSession, id: int, password: str):
        stmt = select(SystemUser).where(SystemUser.id == id, SystemUser.deleted == 0)
        user = (await db.execute(stmt)).scalar_one_or_none()
        if user:
            user.password = hash_password(password)
            await db.commit()
            await db.commit()

    @staticmethod
    async def get_user_profile(db: AsyncSession, id: int):
        user_dict = await UserService.get_user(db, id)
        if not user_dict:
            return None
        return user_dict

    @staticmethod
    async def update_user_profile(db: AsyncSession, id: int, req: UserProfileUpdateReqVO):
        stmt = select(SystemUser).where(SystemUser.id == id)
        user = (await db.execute(stmt)).scalar_one_or_none()
        if not user:
             raise Exception("用户不存在")
        
        data = req.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(user, key, value)
        await db.commit()

    @staticmethod
    async def update_user_avatar(db: AsyncSession, id: int, avatar: str):
        stmt = select(SystemUser).where(SystemUser.id == id)
        user = (await db.execute(stmt)).scalar_one_or_none()
        if user:
            user.avatar = avatar
            await db.commit()

    @staticmethod
    async def get_user_simple_list(db: AsyncSession):
        stmt = select(SystemUser.id, SystemUser.nickname).where(
            SystemUser.deleted == 0,
            SystemUser.status == 0
        )
        result = await db.execute(stmt)
        return result.all()
