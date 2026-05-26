#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project : app
@File    : users.py
@IDE     : PyCharm
@Author  : Jinjing
@Date    : 2026/5/19 17:18
@Desc    :
资产管理 - 用户管理
"""
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from authens import current_user
from database import get_db
from enums import UserStatusEnum
from models import Users, Departments
from schemas import ShowUsers, UpdateUsers, CreateUser, Page

router = APIRouter(
    prefix="/employee",
    tags=["员工管理"]
)


@router.post("/add", response_model=ShowUsers, summary="添加员工")
async def create_employee(
        add_employee: CreateUser,
        user: Users = Depends(current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    添加员工
    权限：登陆的用户
    :return:
    """
    stmt = select(Users).options(selectinload(Users.department)).where(Users.email == add_employee.email)
    result = await db.execute(stmt)
    exist_user = result.scalar_one_or_none()
    if exist_user:
        raise HTTPException(status_code=400, detail="邮箱已存在,请重新添加")

    user_data = add_employee.dict(exclude={"department_name"})          # 排除掉department_name,因为sqlalchemy模型没这个字段
    department_id = None
    # 如果部门存在，则添加部门id
    if add_employee.department_name:
        stmt = select(Departments).where(Departments.name == add_employee.department_name)
        result = await db.execute(stmt)
        department = result.scalar_one_or_none()
        if not department:
            raise HTTPException(status_code=404, detail="部门不存在")
        department_id = department.id
    # 添加员工
    new_user = Users(**user_data, department_id=department_id)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user, attribute_names=["department"])
    return new_user


@router.get("/", response_model=Page[ShowUsers], summary="查看所有员工")
async def show_employees(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1),
        user: Users = Depends(current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    先检查是否是登录用户
    查看所有员工
    :return:
    """
    # 不需要写， current_user会自动检查
    # if not user or user is None:
    #     raise HTTPException(status_code=401, detail="用户未登录")

    # 总数
    total_stmt = select(func.count()).select_from(Users)
    total = (await db.execute(total_stmt)).scalar()
    # 查询所有员工
    stmt = select(Users).options(selectinload(Users.department), selectinload(Users.computers)).offset(skip).limit(limit)
    result = await db.execute(stmt)
    users = result.scalars().all()
    return Page(total=total, data=users)


@router.get('/search', response_model=Page[ShowUsers], summary="搜索包含某个字的员工")
async def search_employee(
        keyword: str,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1),
        user: Users = Depends(current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    模糊查询
    权限: 登录的用户
    :return:查询的用户信息
    """
    # 添加模糊查询条件
    condition = (
        Users.name.like(f"%{keyword}%") |
        Users.email.like(f"%{keyword}%") |
        Users.english_name.like(f"%{keyword}%")
    )
    # 分页总数
    total_stmt = select(func.count()).select_from(Users).where(condition)
    total = (await db.execute(total_stmt)).scalar()
    # 分页的数据
    stmt = (select(Users)
            .options(selectinload(Users.department), selectinload(Users.computers))
            .where(condition)
            .offset(skip)
            .limit(limit)
            )
    result = await db.execute(stmt)
    users = result.scalars().all()
    return Page(total=total, data=users)


@router.put("/{user_name}", response_model=ShowUsers, summary="修改员工信息")
async def update_employee(
        user_name: str,
        update_user: UpdateUsers,
        current: Users = Depends(current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    修改员工信息
    权限：超级管理员
    :return:更新后的用户信息
    """
    # 先验证用户是否是超级用户
    if not current.is_supper:
        raise HTTPException(status_code=401, detail="用户权限不足")
    # 验证用户输入的员工名是否存在
    stmt = select(Users).options(selectinload(Users.department)).where(Users.name == user_name)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    # 更新用户信息
    update_user_data = update_user.dict(exclude_unset=True)
    # 验证邮箱一致性
    if 'email' in update_user_data and update_user_data['email'] != user.email:
        # 检查邮箱是否已经存在
        email_exists = await db.execute(select(Users).where(Users.email == update_user_data['email']))
        if email_exists.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="邮箱已经存在")
    # 验证部门是否存在
    if 'department_id' in update_user_data and update_user_data['department_id'] is not None:
        # 检查部门是否存在
        department_exists = await db.get(Departments, update_user_data['department_id'])
        if not department_exists:
            raise HTTPException(status_code=404, detail="部门不存在")
    # 检查状态合法值
    if 'status' in update_user_data:
        try:
            UserStatusEnum(update_user_data['status'])
        except ValueError:
            raise HTTPException(status_code=401, detail="状态值不合法")

    for key, value in update_user_data.items():
        if hasattr(user, key):
            setattr(user, key, value)
    await db.commit()
    await db.refresh(user, attribute_names=['department', 'computers'])
    return user


@router.delete("/{user_name}", summary="删除员工", status_code=204)
async def delete_employee(
        user_name: str,
        current: Users = Depends(current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    删除员工
    权限：超级管理员
    :return:
    .options(selectinload(Users.department))
    """
    # 先验证登录的用户是否是超级用户
    if not current.is_supper:
        raise HTTPException(status_code=403, detail="用户权限不足")
    # 验证用户输入的员工名是否存在
    stmt = select(Users).where(Users.name == user_name)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if current.name == user_name:
        raise HTTPException(status_code=403, detail="不能删除自己")

    # 删除员工  标记状态为离职，设置离职时间
    user.status = UserStatusEnum.NOTWORK
    user.deleted_at = datetime.now()
    await db.commit()
    return {"message": "删除成功"}
