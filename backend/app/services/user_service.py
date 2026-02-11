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

    @staticmethod
    async def export_users(db: AsyncSession, req: UserPageReqVO):
        from app.models.dept import SystemDept
        from app.utils.excel import ExcelUtils
        
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
            
        result = await db.execute(stmt)
        rows = result.all()
        
        fields = {
            "username": "登录名称",
            "nickname": "用户名称",
            "dept_name": "部门",
            "email": "用户邮箱",
            "mobile": "手机号码",
            "sex": "用户性别",
            "status": "账号状态",
            "create_time": "创建时间"
        }
        
        data = []
        for row in rows:
            u = row[0]
            d_name = row[1]
            data.append({
                "username": u.username,
                "nickname": u.nickname,
                "dept_name": d_name,
                "email": u.email,
                "mobile": u.mobile,
                "sex": "男" if u.sex == 1 else "女" if u.sex == 2 else "未知",
                "status": "开启" if u.status == 0 else "关闭",
                "create_time": u.create_time
            })
            
        return ExcelUtils.write(data, fields, "用户数据")

    @staticmethod
    async def get_import_template():
        from app.utils.excel import ExcelUtils
        fields = {
            "username": "登录名称",
            "nickname": "用户名称",
            "dept_id": "部门编号",
            "email": "用户邮箱",
            "mobile": "手机号码",
            "sex": "用户性别",
            "status": "账号状态"
        }
        data = [
            {
                "username": "yunai",
                "nickname": "芋道",
                "dept_id": 1,
                "email": "yunai@iocoder.cn",
                "mobile": "15601691300",
                "sex": "1",
                "status": "0"
            },
            {
                "username": "yuanma",
                "nickname": "源码",
                "dept_id": 2,
                "email": "yuanma@iocoder.cn",
                "mobile": "15601701300",
                "sex": "2",
                "status": "1"
            }
        ]
        return ExcelUtils.write(data, fields, "用户导入模板")

    @staticmethod
    async def import_users(db: AsyncSession, file_content: bytes, update_support: bool):
        from app.utils.excel import ExcelUtils
        from app.schemas.user import UserImportExcelVO
        fields = {
            "登录名称": "username",
            "用户名称": "nickname",
            "部门编号": "dept_id",
            "用户邮箱": "email",
            "手机号码": "mobile",
            "用户性别": "sex",
            "账号状态": "status"
        }
        import_data = ExcelUtils.read(file_content, UserImportExcelVO, fields)
        
        create_usernames = []
        update_usernames = []
        failure_usernames = {}
        
        for item in import_data:
            username = item.get("username")
            if not username:
                continue
            
            try:
                stmt = select(SystemUser).where(SystemUser.username == username, SystemUser.deleted == 0)
                existing_user = (await db.execute(stmt)).scalar_one_or_none()
                
                if existing_user:
                    if not update_support:
                        failure_usernames[username] = "用户已存在"
                        continue
                    # Update
                    for key, value in item.items():
                        if value is not None:
                            setattr(existing_user, key, value)
                    existing_user.updater = "admin"
                    update_usernames.append(username)
                else:
                    # Create
                    new_user = SystemUser(
                        **item,
                        password=hash_password("123456"),
                        tenant_id=0,
                        creator="admin",
                        updater="admin"
                    )
                    db.add(new_user)
                    create_usernames.append(username)
            except Exception as e:
                failure_usernames[username] = str(e)
        
        await db.commit()
        return {
            "create_usernames": create_usernames,
            "update_usernames": update_usernames,
            "failure_usernames": failure_usernames
        }
