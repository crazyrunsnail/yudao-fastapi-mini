from functools import wraps
from fastapi import Request
from typing import Optional
from app.services.log_service import LogService
from app.utils.request import get_user_ip, get_user_agent
from app.core.context import get_trace_id, get_operate_log_vars, clear_operate_log_vars
import json

def operate_log(type: str, sub_type: str, biz_id_field: Optional[str] = None):
    """
    操作日志装饰器
    :param type: 操作模块类型
    :param sub_type: 操作名
    :param biz_id_field: 业务 ID 字段名
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            if not request:
                # 从 args 中寻找 Request 对象
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            
            db = kwargs.get("db")
            user = kwargs.get("user") or kwargs.get("current_user")
            
            # 清理之前的变量
            clear_operate_log_vars()
            
            result = None
            exception = None
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                exception = e
                raise e
            finally:
                if request and db:
                    try:
                        # 获取动态上下文变量
                        vars = get_operate_log_vars()
                        
                        method = request.method
                        log_data = {
                            "trace_id": get_trace_id(),
                            "user_id": user.id if user else (user.userId if hasattr(user, 'userId') else 0),
                            "user_type": 1,
                            "type": type,
                            "sub_type": sub_type,
                            "biz_id": 0,
                            "action": f"{type}-{sub_type}",
                            "success": exception is None,
                            "request_method": method,
                            "request_url": str(request.url),
                            "user_ip": get_user_ip(request),
                            "user_agent": get_user_agent(request),
                            "extra": json.dumps(vars, ensure_ascii=False) if vars else ""
                        }
                        
                        # 解析业务 ID
                        if biz_id_field:
                            if biz_id_field in kwargs:
                                try:
                                    log_data["biz_id"] = int(kwargs[biz_id_field])
                                except: pass
                            elif "req" in kwargs and hasattr(kwargs["req"], biz_id_field):
                                try:
                                    log_data["biz_id"] = int(getattr(kwargs["req"], biz_id_field))
                                except: pass
                        elif "id" in kwargs:
                            try:
                                log_data["biz_id"] = int(kwargs["id"])
                            except: pass
                        elif "req" in kwargs and hasattr(kwargs["req"], "id"):
                            try:
                                log_data["biz_id"] = int(getattr(kwargs["req"], "id"))
                            except: pass
                            
                        # 如果业务逻辑中手动设置了 biz_id
                        if "biz_id" in vars:
                            log_data["biz_id"] = vars["biz_id"]
                        
                        import logging
                        logging.info(f"Attempting to record operate log: {type}-{sub_type}")
                        await LogService.create_operate_log(db, log_data)
                        logging.info(f"Successfully recorded operate log: {type}-{sub_type}")
                    except Exception as log_err:
                        import logging
                        logging.error(f"Failed to record operate log: {str(log_err)}")
                        import traceback
                        logging.error(traceback.format_exc())
                else:
                    import logging
                    logging.warning(f"Skipping operate log for {type}-{sub_type} because request={bool(request)} or db={bool(db)} is missing")
        
        return wrapper
    return decorator
