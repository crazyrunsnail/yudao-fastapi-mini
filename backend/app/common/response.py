from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel

DataT = TypeVar("DataT")

class CommonResult(BaseModel, Generic[DataT]):
    code: int = 0
    data: Optional[DataT] = None
    msg: str = ""

    @classmethod
    def success(cls, data: Any = None, msg: str = "") -> "CommonResult":
        return cls(code=0, data=data, msg=msg)

    @classmethod
    def error(cls, code: int = 500, msg: str = "Internal Server Error") -> "CommonResult":
        return cls(code=code, msg=msg)
