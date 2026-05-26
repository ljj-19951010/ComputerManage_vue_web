#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project : app
@File    : monitors.py
@IDE     : PyCharm
@Author  : Jinjing
@Date    : 2026/5/19 17:18
@Desc    :
显示器
"""
from datetime import datetime

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from authens import current_user
from database import get_db
from enums import AssetTypeEnum, ActionEnum, MonitorsStatus, OperatorTypeEnum
from models import Monitors, Users
from schemas import Page, ShowMonitors, CreateMonitors, UpdateMonitors
from untils.asset_logger import log_asset_operation

router = APIRouter(
    prefix='/monitors',
    tags=['显示器'],
)


@router.post('/add', response_model=ShowMonitors, summary="添加显示器")
async def add_monitor(
        add_monitor: CreateMonitors,
        current: Users = Depends(current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    添加显示器
    权限:登录的用户
    :param add_monitor:
    :param current:
    :param db:
    :return:
    """
    stmt = select(Monitors).options(selectinload(Monitors.model), selectinload(Monitors.user)).where((Monitors.asset_tag==add_monitor.asset_tag) | (Monitors.serial_number==add_monitor.serial_number))
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="显示器已存在")
    monitor_data = add_monitor.dict(exclude={"employee_id", "employee_name"})
    new_monitor = Monitors(**monitor_data, user_id=add_monitor.employee_id)
    db.add(new_monitor)
    await db.flush()
    # 日志记录
    await log_asset_operation(
        db=db,
        asset_type=AssetTypeEnum.MONITOR,
        asset_id=new_monitor.id,
        action=ActionEnum.CREATE,
        operator_id=current.id,
        operator_type='admin' if current.is_supper else 'user',
        new_value={"asset_tag": new_monitor.asset_tag, "serial_number": new_monitor.serial_number},
        remark=f"用户{current.username}添加资产编号为{new_monitor.asset_tag}的显示器"
    )
    await db.commit()
    await db.refresh(new_monitor, attribute_names=['user'])
    return new_monitor


@router.get('/', response_model=Page[ShowMonitors], summary="查看所有显示器")
async def get_monitors(
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=10, ge=1, le=100),
        db: AsyncSession = Depends(get_db)
):
    """
    查看所有显示器
    权限:任何人
    :return:
    """
    # 查询总数
    total_stmt = select(func.count()).select_from(Monitors)
    total = (await db.execute(total_stmt)).scalar()

    # 查询数据
    stmt = select(Monitors).options(selectinload(Monitors.model), selectinload(Monitors.user)).offset(skip).limit(limit)
    result = await db.execute(stmt)
    monitors = result.scalars().all()
    return Page(total=total, data=monitors)


@router.get('/search', response_model=Page[ShowMonitors], summary="搜索显示器")
async def search_monitors(
        keywords: str = Query(default=None, description="关键词"),
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=10, ge=1, le=100),
        current: Users = Depends(current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    模糊查询
    权限:登录的用户
    :return:
    """
    if not keywords:
        raise HTTPException(status_code=400, detail="关键词不能为空")

    # 查询条件
    condition = (
        Monitors.asset_tag.like(f'%{keywords}%') |
        Monitors.serial_number.like(f'%{keywords}%') |
        Monitors.user.has(Users.name.like(f'%{keywords}%'))
    )
    # 预加载模型关联对象
    stmt = select(Monitors).options(selectinload(Monitors.model), selectinload(Monitors.user))
    # 查询总数
    total_stmt = select(func.count()).select_from(Monitors).where(condition)
    total = (await db.execute(total_stmt)).scalar()
    # 查询数据
    result_stmt = stmt.where(condition).offset(skip).limit(limit)
    result = await db.execute(result_stmt)
    monitors = result.scalars().all()
    return Page(total=total, data=monitors)


@router.put('/update/{asset_tags}', response_model=ShowMonitors, summary="更新显示器")
async def update_monitor(
        asset_tags: str,
        update_monitor: UpdateMonitors,
        current: Users = Depends(current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    更新显示器
    权限:登录的用户
    :return:
    """
    stmt = select(Monitors).options(selectinload(Monitors.model), selectinload(Monitors.user)).where((Monitors.asset_tag == asset_tags))
    result = await db.execute(stmt)
    monitor = result.scalar_one_or_none()
    if not monitor:
        raise HTTPException(status_code=404, detail="显示器不存在")

    monitor_data = update_monitor.dict(exclude={"employee_id", "employee_name"}, exclude_unset=True)
    if not monitor_data:
        raise HTTPException(status_code=400, detail="没有需要更新的字段")

    if 'asset_tag' in monitor_data and monitor_data['asset_tag'] != monitor.asset_tag:
        existing = await db.execute(select(Monitors).where(Monitors.asset_tag == monitor_data['asset_tag'], Monitors.id != monitor.id))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="显示器编号已存在")

    if 'serial_number' in monitor_data and monitor_data['serial_number'] != monitor.serial_number:
        existing = await db.execute(select(Monitors).where(Monitors.serial_number == monitor_data['serial_number']))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="显示器序列号已存在")
    if update_monitor.employee_id:
        monitor_data['user_id'] = update_monitor.employee_id
    old_value = {}
    new_value = {}

    for filed, value in monitor_data.items():
        old = getattr(monitor, filed)           # 获取旧数据
        if old != value:            # 如果旧数据不等于新数据
            old_value[filed] = old          # 把旧数据的值添加到字典里
            new_value[filed] = value            # 新数据的值添加到字典里
            setattr(monitor, filed, value)          # 更新数据库

    # 记录日志
    if old_value:
        await log_asset_operation(
            db=db,
            asset_type=AssetTypeEnum.MONITOR,
            asset_id=monitor.id,
            action=ActionEnum.UPDATE,
            operator_id=current.id,
            operator_type='admin' if current.is_supper else 'user',
            old_value=old_value,
            new_value=new_value,
            remark=f'用户{current.username}更新资产编号为{monitor.asset_tag}的信息'
        )
        await db.commit()
    await db.refresh(monitor)
    return monitor


@router.delete('/delete', summary="删除显示器", status_code=204)
async def delete_monitor(
        asset_tags: str,
        current: Users = Depends(current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    删除显示器
    权限:超级管理员用户
    :return:
    """
    if not current.is_supper:
        raise HTTPException(status_code=403, detail="无权限")
    stmt = select(Monitors).options(selectinload(Monitors.model), selectinload(Monitors.user)).where((Monitors.asset_tag == asset_tags))
    result = await db.execute(stmt)
    monitor = result.scalar_one_or_none()
    if not monitor:
        raise HTTPException(status_code=404, detail="显示器不存在")
    if monitor.status == MonitorsStatus.DELETED:
        raise HTTPException(status_code=400, detail="显示器已经被删除")
    if monitor.deleted_at:
        raise HTTPException(status_code=400, detail="显示器已经被删除")
    monitor.deleted_at = datetime.now()
    monitor.status = MonitorsStatus.DELETED
    await log_asset_operation(
        db=db,
        asset_type=AssetTypeEnum.MONITOR,
        asset_id=monitor.id,
        action=ActionEnum.DELETE,
        operator_id=current.id,
        operator_type=OperatorTypeEnum.ADMIN,
        new_value={"deleted_at": monitor.deleted_at},
        remark=f'用户{current.username}删除资产编号为{monitor.asset_tag}的信息'
    )
    await db.commit()
    await db.refresh(monitor)
    return {'message': '删除成功'}
