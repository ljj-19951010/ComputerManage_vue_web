#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project : app
@File    : computers.py
@IDE     : PyCharm
@Author  : Jinjing
@Date    : 2026/5/19 17:18
@Desc    :
笔记本电脑
"""
from datetime import datetime


from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from authens import current_user
from database import get_db
from enums import ComputersStatus, AssetTypeEnum, OperatorTypeEnum
from models import Users, Computers
from schemas import ShowComputers, Page, CreateComputers, UpdateComputers
from untils.asset_logger import log_asset_operation

router = APIRouter(
    prefix='/computers',
    tags=['电脑'],
)


@router.post('/add', response_model=ShowComputers, summary='添加电脑')
async def add_computer(
        add_computer: CreateComputers,
        current: Users = Depends(current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    添加电脑
    权限:登录的用户
    :param add_computer: 输入的电脑信息
    :param current: 登陆的用户
    :param db: 数据库
    :return:
    """
    stmt = select(Computers).options(selectinload(Computers.user), selectinload(Computers.model)).where((Computers.asset_tag == add_computer.asset_tag) | (Computers.serial_number == add_computer.serial_number))
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail='电脑已存在')
    # 排除SQLalchemy中没有的字段
    computer_data = add_computer.dict(exclude={"employee_id", "employee_name"})

    new_computer = Computers(**computer_data, user_id=add_computer.employee_id)
    db.add(new_computer)
    await db.flush()
    # 日志记录
    await log_asset_operation(
        db=db,
        asset_type=AssetTypeEnum.COMPUTER,
        asset_id=new_computer.id,
        action='add',
        operator_id=current.id,
        operator_type='admin' if current.is_supper else 'user',
        new_value={"asset_tag": new_computer.asset_tag, "serial_number": new_computer.serial_number},
        remark=f"用户{current.username}添加资产编号为{new_computer.asset_tag}的电脑"
    )
    await db.commit()
    await db.refresh(new_computer, attribute_names=['user'])
    return new_computer


@router.get('/', response_model=Page[ShowComputers], summary='查看所有电脑')
async def show_computers(
        skip: int = Query(default=0, ge=0, description='跳过条数'),
        limit: int = Query(default=10, ge=1, le=100, description='每页条数'),
        db: AsyncSession = Depends(get_db)
):
    """
    查看所有电脑信息
    不需要权限
    :param skip: 跳过几条
    :param limit: 每页数据
    :param db: 数据库
    :return:
    """
    # 查询总数
    total_stmt = select(func.count()).select_from(Computers)
    total = (await db.execute(total_stmt)).scalar()
    # 查询数据
    stmt = select(Computers).options(selectinload(Computers.model), selectinload(Computers.user)).offset(skip).limit(limit)
    result = await db.execute(stmt)
    computer = result.scalars().all()
    return Page(total=total, data=computer)


@router.get('/search', response_model=Page[ShowComputers], summary='搜索电脑')
async def search_computers(
        keywords: str,
        skip: int = Query(default=0, ge=0, description='跳过几条'),
        limit: int = Query(default=10, ge=1, le=100, description='每页条数'),
        current: Users = Depends(current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    搜索电脑
    权限:已登录用户
    :return:
    """
    # 包装查询条件
    condition = (
        Computers.asset_tag.like(f'%{keywords}%') |
        Computers.serial_number.like(f'%{keywords}%') |
        Computers.user.has(Users.name.like(f'%{keywords}%'))
    )
    stmt = select(Computers).options(selectinload(Computers.model), selectinload(Computers.user))
    total_stmt = select(func.count()).select_from(Computers).where(condition)
    total = (await db.execute(total_stmt)).scalar()

    data_stmt = stmt.where(condition).offset(skip).limit(limit)
    result = await db.execute(data_stmt)
    computers = result.scalars().all()
    return Page(total=total, data=computers)


@router.put('/update/{asset_tag}', response_model=ShowComputers, summary='更新电脑信息')
async def update_computer(
        asset_tag: str,
        update_computer: UpdateComputers,
        current: Users = Depends(current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    更新电脑信息
    权限:登录的用户
    :return:
    """
    stmt = select(Computers).options(selectinload(Computers.user)).where(Computers.asset_tag == asset_tag)
    result = await db.execute(stmt)
    computer = result.scalar_one_or_none()
    if not computer:
        raise HTTPException(status_code=404, detail='电脑不存在')
    old_value = {}
    new_value = {}

    computer_data = update_computer.dict(exclude_unset=True, exclude={'employee_id', 'employee_name'})
    if not computer_data:
        raise HTTPException(status_code=400, detail='没有需要更新的字段')
    # 检查序列号是否存在
    if 'serial_number' in computer_data and computer_data['serial_number'] != computer.serial_number:
        existing = await db.execute(select(Computers).where(Computers.serial_number == computer_data['serial_number'], Computers.id != computer.id))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail='序列号已存在')
    # 检查资产标签是否存在
    if 'asset_tag' in computer_data and computer_data['asset_tag'] != computer.asset_tag:
        existing = await db.execute(select(Computers).where(Computers.asset_tag == computer_data['asset_tag'], Computers.id != computer.id))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail='资产标签已存在')
    computer_data['user_id'] = update_computer.employee_id

    for filed, new_val in computer_data.items():
        old_val = getattr(computer, filed)
        if old_val != new_val:
            old_value[filed] = old_val
            new_value[filed] = new_val
            setattr(computer, filed, new_val)
    # 记录日志
    if old_value:
        await log_asset_operation(
            db=db,
            asset_type=AssetTypeEnum.COMPUTER,
            asset_id=computer.id,
            action='update',
            operator_id=current.id,
            operator_type='admin' if current.is_supper else 'user',
            old_value=old_value,
            new_value=new_value,
            remark=f'用户{current.username}更新资产编号为{computer.asset_tag}的信息'
        )
        await db.commit()
    await db.refresh(computer)
    return computer


@router.delete('/del', summary='删除电脑')
async def delete_computer(
        asset_tag: str,
        current: Users = Depends(current_user),
        db: AsyncSession = Depends(get_db)
):
    if not current.is_supper:
        raise HTTPException(status_code=403, detail='没有权限')

    stmt = select(Computers).options(selectinload(Computers.user)).where(Computers.asset_tag == asset_tag)
    result = await db.execute(stmt)
    computer = result.scalar_one_or_none()
    if not computer:
        raise HTTPException(status_code=404, detail='电脑不存在')
    if computer.status == ComputersStatus.DELETED:
        raise HTTPException(status_code=400, detail='电脑已删除')

    computer.deleted_at = datetime.now()
    computer.status = ComputersStatus.DELETED
    await log_asset_operation(
        db=db,
        asset_type=AssetTypeEnum.COMPUTER,
        asset_id=computer.id,
        action='delete',
        operator_id=current.id,
        operator_type=OperatorTypeEnum.ADMIN,
        new_value={"deleted_at": computer.deleted_at},
        remark=f'用户{current.username}删除了资产编号为{computer.asset_tag}的电脑'
    )
    await db.commit()
    await db.refresh(computer)
    return {"message": "删除成功"}
