from fastapi import Request

def get_user_ip(request: Request) -> str:
    """获取用户 IP"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]
    return request.client.host if request.client else "127.0.0.1"

def get_user_agent(request: Request) -> str:
    """获取用户 User-Agent"""
    return request.headers.get("User-Agent", "")
