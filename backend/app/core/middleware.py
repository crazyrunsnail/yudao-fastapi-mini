from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid
from app.core.context import set_trace_id

class TraceIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 优先从 Header 获取，如果没有则生成
        tid = request.headers.get("X-Trace-Id") or str(uuid.uuid4()).replace("-", "")
        set_trace_id(tid)
        
        response = await call_next(request)
        
        # 将 TraceId 返回给前端
        response.headers["X-Trace-Id"] = tid
        return response
