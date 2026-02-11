from fastapi import APIRouter, Depends, Header, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.auth import AuthLoginReqVO, AuthLoginRespVO, AuthPermissionInfoRespVO, UserInfoVO
from app.services.auth_service import AuthService
from app.services.menu_service import MenuService
from app.models.user import SystemUser
from sqlalchemy import select
from app.common.response import CommonResult
from typing import Optional
from app.services.log_service import LogService
from app.utils.request import get_user_ip, get_user_agent
from fastapi import HTTPException
from app.enums.system_enums import LoginLogTypeEnum, LoginResultEnum

router = APIRouter(prefix="/system/auth", tags=["管理后台 - 认证"])

from app.core.context import get_trace_id

@router.post("/login", response_model=CommonResult[AuthLoginRespVO])
async def login(request: Request, req: AuthLoginReqVO, db: AsyncSession = Depends(get_db)):
    user_ip = get_user_ip(request)
    user_agent = get_user_agent(request)
    trace_id = get_trace_id()
    try:
        result = await AuthService.login(db, req)
        # 记录成功日志
        await LogService.create_login_log(db, {
            "log_type": LoginLogTypeEnum.LOGIN_USERNAME, 
            "trace_id": trace_id,
            "username": req.username,
            "user_ip": user_ip,
            "user_agent": user_agent,
            "result": LoginResultEnum.SUCCESS, 
            "user_id": result.user_id,
            "user_type": 1 
        })
        return CommonResult.success(data=result)
    except HTTPException as e:
        # 映射登录结果枚举
        login_result = LoginResultEnum.BAD_CREDENTIALS # 默认账号密码错误
        if "禁用" in str(e.detail):
            login_result = LoginResultEnum.USER_DISABLED
            
        # 记录失败日志
        await LogService.create_login_log(db, {
            "log_type": LoginLogTypeEnum.LOGIN_USERNAME,
            "trace_id": trace_id,
            "username": req.username,
            "user_ip": user_ip,
            "user_agent": user_agent,
            "result": login_result,
            "user_id": 0,
            "user_type": 1
        })
        raise e

@router.post("/logout", response_model=CommonResult[bool])
async def logout(request: Request, authorization: Optional[str] = Header(None), db: AsyncSession = Depends(get_db)):
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        from app.services.token_service import TokenService
        token_data = await TokenService.get_access_token(db, token)
        if token_data:
            user_id = token_data.get("userId")
            # 记录登出日志
            await LogService.create_login_log(db, {
                "log_type": LoginLogTypeEnum.LOGOUT_SELF, 
                "trace_id": get_trace_id(),
                "username": "", 
                "user_ip": get_user_ip(request),
                "user_agent": get_user_agent(request),
                "result": LoginResultEnum.SUCCESS,
                "user_id": user_id,
                "user_type": 1
            })
        await AuthService.logout(db, token)
    return CommonResult.success(data=True)


@router.post("/refresh-token", response_model=CommonResult[AuthLoginRespVO])
async def refresh_token(request: Request, refreshToken: str = Query(...), db: AsyncSession = Depends(get_db)):
    result = await AuthService.refresh_token(db, refreshToken)
    return CommonResult.success(data=result)


from app.core.auth import get_login_user
from app.services.permission_service import PermissionService
from app.services.role_service import RoleService

@router.get("/get-permission-info", response_model=CommonResult[AuthPermissionInfoRespVO])
async def get_permission_info(
    user: SystemUser = Depends(get_login_user),
    db: AsyncSession = Depends(get_db)
):
    # 1. 获取角色代码
    role_ids = await PermissionService.get_user_role_ids(db, user.id)
    roles = []
    for rid in role_ids:
        role = await RoleService.get_role(db, rid)
        if role and role.status == 0:
            roles.append(role.code)
            
    # 2. 获取权限标识
    is_super = "super_admin" in roles
    if is_super:
        permissions = ["*:*:*"]
        all_menus = await MenuService.get_all_menus(db)
    else:
        permissions = list(await PermissionService.get_user_permissions(db, user.id))
        # 获取用户有权访问的菜单
        menu_ids = await PermissionService.get_role_menu_ids_by_role_ids(db, role_ids)
        all_menus = await MenuService.get_menu_list_by_ids(db, list(menu_ids))
        
    
    # 3. 构建菜单树
    # 过滤掉按钮类型的菜单 (type=3)
    # type: 1 目录, 2 菜单, 3 按钮
    visible_menus = [menu for menu in all_menus if menu.type != 3]
    menu_tree = await MenuService.build_menu_tree(visible_menus)
    
    # 4. 修正 alwaysShow：如果节点没有子菜单，强制设置 alwaysShow=False
    # 否则前端会因为 alwaysShow=true 而渲染成空的下拉菜单
    def fix_menu_tree(menus):
        if not menus:
            return
        for menu in menus:
            if not menu.children:  # None 或 []
                menu.always_show = False
            else:
                fix_menu_tree(menu.children)
    
    fix_menu_tree(menu_tree)
    
    return CommonResult.success(data=AuthPermissionInfoRespVO(
        user=UserInfoVO(
            id=user.id,
            nickname=user.nickname,
            avatar=user.avatar or "",
            username=user.username
        ),
        roles=roles,
        permissions=permissions, 
        menus=menu_tree
    ))
