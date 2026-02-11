import contextvars
from typing import Dict, Any, Optional

# 链路追踪 ID
trace_id: contextvars.ContextVar[str] = contextvars.ContextVar("trace_id", default="")

# 操作日志变量
operate_log_vars: contextvars.ContextVar[Dict[str, Any]] = contextvars.ContextVar("operate_log_vars", default={})

def get_trace_id() -> str:
    return trace_id.get()

def set_trace_id(tid: str):
    trace_id.set(tid)

def get_operate_log_vars() -> Dict[str, Any]:
    return operate_log_vars.get()

def set_operate_log_var(name: str, value: Any):
    vars = operate_log_vars.get().copy()
    vars[name] = value
    operate_log_vars.set(vars)

def clear_operate_log_vars():
    operate_log_vars.set({})
