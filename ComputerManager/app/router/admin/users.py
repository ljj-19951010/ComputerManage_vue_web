#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project : app
@File    : users.py
@IDE     : PyCharm
@Author  : Jinjing
@Date    : 2026/5/19 17:18
@Desc    :
后台管理系统
"""
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from authens import get_password_hash, verify_password, create_token, current_user, oauth2
from database import get_db
from models import Admins
from schemas import ShowAdmins, CreateAdmins, Token, UpdateAdmins

# 路由
router = APIRouter(
    prefix='/admin',
    tags=['后台管理']
)


# 注册
@router.post('/register', response_model=ShowAdmins, summary='注册系统')
async def register_admin(
        user_in: CreateAdmins,
        db: AsyncSession = Depends(get_db)
):
    stmt = select(Admins).where((Admins.username == user_in.username) | (Admins.email == user_in.email))
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()
    if existing:
        if existing.username == user_in.username:
            raise HTTPException(status_code=400, detail="用户名已经存在")
        else:
            raise HTTPException(status_code=400, detail="邮箱已经存在")
    # 创建用户
    user_data = user_in.dict(exclude={"password"})          # 获取除了密码以外的数据
    new_user = Admins(**user_data)          # 创建用户
    new_user.password_hash = get_password_hash(user_in.password)        # 加密密码
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


# 登录
@router.post('/login', response_model=Token, summary='登录系统')
async def login_admin(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    stmt = select(Admins).where(Admins.email == form_data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        stmt = select(Admins).where(Admins.username == form_data.username)
        user = (await db.execute(stmt)).scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    if not user.is_active or user.is_delete:
        raise HTTPException(status_code=400, detail="用户已被禁用或删除")

    user.last_login_at = datetime.now()
    await db.commit()

    # 生成token
    user_id = user.id           # 比以前的多加了id，所以需要这样添加
    username = user.username
    token_payload = {
        "user_id": user_id,
        "username": username
    }
    create_access_token = await create_token(token_payload)
    return {"access_token": create_access_token, "token_type": "bearer"}


@router.get('/', response_model=List[ShowAdmins], summary='查看所有用户信息')
async def show_all_admins(
        current: Admins = Depends(current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    查看所有用户信息
    权限：超级管理员
    :param db:
    :return:
    """
    if not current.is_supper:
        raise HTTPException(status_code=403, detail="没有权限")

    result = await db.execute(select(Admins))
    user = result.scalars().all()
    return user


@router.put('/{username}', response_model=ShowAdmins, summary='修改用户信息')
async def update_admin(
        username: str,
        user_in: UpdateAdmins,
        current: Admins = Depends(current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    更新用户，用户名唯一不能更改
    :param username:
    :param user_in:
    :param db:
    :return:
    """
    # 查看当前用户是否为超级用户
    if not current.is_supper:
        raise HTTPException(status_code=403, detail="没有权限")
    # 否则是超级用户，可以更新用户
    # 从数据库中查询用户
    stmt = select(Admins).where(Admins.username == username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    # 查询用户是否存在
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在或输入的账户错误")
    # 检查邮箱唯一性
    if user_in.email and user_in.email != user.email:
        stmt = select(Admins).where(Admins.email == user_in.email)
        result = await db.execute(stmt)
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="邮箱已经存在")

    # 更新用户信息
    user_in_data = user_in.dict(exclude={"password"}, exclude_unset=True)
    if user_in.password:
        user_in_data['password_hash'] = get_password_hash(user_in.password)
    for key, value in user_in_data.items():
        if hasattr(user, key):
            setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user


@router.delete('/del/{username}', summary='删除用户', status_code=204)
async def delete_admin(
        username: str,
        current: Admins = Depends(current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    删除管理员
    权限：只能是超级管理员
    :return:
    """
    # 查看当前用户是否为超级用户
    if not current.is_supper:
        raise HTTPException(status_code=403, detail="没有权限")
    # 否则是超级用户，可以删除用户
    # 从数据库中查询用户
    stmt = select(Admins).where(Admins.username == username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    # 查询用户是否存在
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在或输入的账户错误")
    if current.username == username:
        raise HTTPException(status_code=400, detail="不能删除自己")
    # 删除用户
    user.is_delete = True
    user.is_active = False
    await db.commit()
    await db.refresh(user)
    return {"msg": "删除成功"}
