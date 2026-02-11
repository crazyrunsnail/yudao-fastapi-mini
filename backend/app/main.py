from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.common.response import CommonResult
from app.api.system.auth import router as auth_router
from app.api.system.tenant import router as tenant_router
from app.api.system.user import router as user_router
from app.api.system.dept import router as dept_router
from app.api.system.post import router as post_router
from app.api.system.role import router as role_router
from app.api.system.notify import router as notify_router
from app.api.system.notify_template import router as notify_template_router
from app.api.system.notice import router as notice_router
from app.api.system.menu import router as menu_router
from app.api.system.permission import router as permission_router
from app.api.system.dict_type import router as dict_type_router
from app.api.system.dict_data import router as dict_data_router
from app.api.system.login_log import router as login_log_router
from app.api.system.operate_log import router as operate_log_router
from app.api.system.tenant_package import router as tenant_package_router
from app.api.system.user_profile import router as user_profile_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # 401 错误码在 RuoYi/Yudao 中是特定的，用于触发刷新 Token 或重定向到登录
    # 前端 axios 拦截器通常只处理 200 响应中的 code=401，所以这里 status_code 返回 200
    return JSONResponse(
        status_code=200,
        content={"code": exc.status_code, "msg": exc.detail, "data": None}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # 全局异常捕获，返回 500
    print(f"Global Exception: {str(exc)}")
    import traceback
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"code": 500, "msg": "系统内部错误", "data": None}
    )

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
         return JSONResponse(
            status_code=404,  # 可以根据前端是否需要 200 来调整，通常 404 保持 404 即可，或者也改成 200 + code=404
            content={"code": 404, "msg": "请求地址不存在", "data": None}
        )
    return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"code": 400, "msg": "请求参数错误", "data": str(exc)}
    )

# 设置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.core.middleware import TraceIdMiddleware
app.add_middleware(TraceIdMiddleware)


# 注册路由
# 前端请求的是 /admin-api/system/auth/...
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(tenant_router, prefix=settings.API_V1_STR)
app.include_router(tenant_package_router, prefix=settings.API_V1_STR)
app.include_router(user_router, prefix=settings.API_V1_STR)
app.include_router(dept_router, prefix=settings.API_V1_STR)
app.include_router(post_router, prefix=settings.API_V1_STR)
app.include_router(role_router, prefix=settings.API_V1_STR)
app.include_router(notify_router, prefix=settings.API_V1_STR)
app.include_router(notify_template_router, prefix=settings.API_V1_STR)
app.include_router(notice_router, prefix=settings.API_V1_STR)
app.include_router(menu_router, prefix=settings.API_V1_STR)
app.include_router(permission_router, prefix=settings.API_V1_STR)
app.include_router(dict_type_router, prefix=settings.API_V1_STR)
app.include_router(dict_data_router, prefix=settings.API_V1_STR)
app.include_router(login_log_router, prefix=settings.API_V1_STR)
app.include_router(operate_log_router, prefix=settings.API_V1_STR)

app.include_router(user_profile_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to Yudao FastAPI Mini"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=48080)
