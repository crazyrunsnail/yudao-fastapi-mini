from fastapi import APIRouter, Depends, Query, Body, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.common.response import CommonResult
from app.schemas.base import PageResult
from app.schemas.post import PostPageReqVO, PostRespVO, PostSaveReqVO, PostSimpleRespVO
from app.services.post_service import PostService
from app.core.auth import has_permission, get_login_user
from app.common.operate_log import operate_log
from typing import List

router = APIRouter(prefix="/system/post", tags=["管理后台 - 岗位"])

@router.get("/page", response_model=CommonResult[PageResult[PostRespVO]], dependencies=[has_permission("system:post:query")])
@operate_log(type="岗位管理", sub_type="查询岗位分页")
async def get_post_page(request: Request, req: PostPageReqVO = Depends(), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    items, total = await PostService.get_post_page(db, req)
    return CommonResult.success(data=PageResult(list=items, total=total))

@router.get("/get", response_model=CommonResult[PostRespVO], dependencies=[has_permission("system:post:query")])
@operate_log(type="岗位管理", sub_type="查看岗位详情", biz_id_field="id")
async def get_post(request: Request, id: int = Query(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    item = await PostService.get_post(db, id)
    return CommonResult.success(data=item)

@router.post("/create", response_model=CommonResult[int], dependencies=[has_permission("system:post:create")])
@operate_log(type="岗位管理", sub_type="新增岗位")
async def create_post(request: Request, req: PostSaveReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    item = await PostService.create_post(db, req)
    return CommonResult.success(data=item.id)

@router.put("/update", response_model=CommonResult[bool], dependencies=[has_permission("system:post:update")])
@operate_log(type="岗位管理", sub_type="修改岗位")
async def update_post(request: Request, req: PostSaveReqVO = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    await PostService.update_post(db, req)
    return CommonResult.success(data=True)

@router.delete("/delete", response_model=CommonResult[bool], dependencies=[has_permission("system:post:delete")])
@operate_log(type="岗位管理", sub_type="删除岗位", biz_id_field="id")
async def delete_post(request: Request, id: int = Query(...), db: AsyncSession = Depends(get_db), user=Depends(get_login_user)):
    await PostService.delete_post(db, id)
    return CommonResult.success(data=True)

@router.get("/simple-list", response_model=CommonResult[List[PostSimpleRespVO]])
async def get_post_simple_list(db: AsyncSession = Depends(get_db)):
    items = await PostService.get_post_simple_list(db)
    return CommonResult.success(data=items)

@router.get("/export-excel", dependencies=[has_permission("system:post:export")])
@operate_log(type="岗位管理", sub_type="导出岗位")
async def export_post(req: PostPageReqVO = Depends(), db: AsyncSession = Depends(get_db)):
    content = await PostService.export_posts(db, req)
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=post_export.xlsx"}
    )
