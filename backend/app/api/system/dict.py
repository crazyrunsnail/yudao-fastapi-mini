from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.common.response import CommonResult
from sqlalchemy import select
from app.models.dict import SystemDictData
from app.schemas.base import BaseSchema
from typing import List, Optional

router = APIRouter(prefix="/system", tags=["管理后台 - 字典"])

class DictDataSimpleRespVO(BaseSchema):
    dict_type: str
    value: str
    label: str
    color_type: Optional[str] = ""
    css_class: Optional[str] = ""

@router.get("/dict-data/simple-list", response_model=CommonResult[List[DictDataSimpleRespVO]])
async def get_dict_data_simple_list(db: AsyncSession = Depends(get_db)):
    # 查询所有开启状态的字典数据
    stmt = select(SystemDictData).where(SystemDictData.status == 0, SystemDictData.deleted == 0)
    result = await db.execute(stmt)
    dict_datas = result.scalars().all()
    
    # 转换为 VO
    resp_list = [
        DictDataSimpleRespVO(
            dict_type=d.dict_type,
            value=d.value,
            label=d.label,
            color_type=d.color_type,
            css_class=d.css_class
        ) for d in dict_datas
    ]
    
    return CommonResult.success(data=resp_list)
