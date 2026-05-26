#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project : app
@File    : authens.py
@IDE     : PyCharm
@Author  : Jinjing
@Date    : 2026/5/19 17:17
@Desc    :
JWT安全验证
"""
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import generate_password_hash, check_password_hash

from config import settings
from database import get_db
from models import Admins
from schemas import TokenData

ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
# 从该路径自动获取token数据
oauth2 = OAuth2PasswordBearer(tokenUrl="/admin/login")


# 创建token
async def create_token(token: dict, expire_delay: timedelta = None):
    """
    只负责编码
    :param token:
    :param expire_delay:
    :return:
    """
    token_copy = token.copy()
    # 如果传入了参数过期时间
    if expire_delay:
        expire = datetime.now(timezone.utc) + expire_delay
    # 如果没传入过期时间，就按配置的过期时间
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 将过期时间添加到字典中
    token_copy.update({"exp": expire})
    # 生成token
    jwt_token = jwt.encode(token_copy, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token


# 验证token
async def verify_token(token: str) -> TokenData:
    """
    负责将/user/login返回的token进行解码
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])         # 获取传过来的token解码
        username: str = payload.get("username")          # 获取用户名
        user_id: int = payload.get("user_id")           # 获取用户id
        if not username or not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"}
            )
        token_data = TokenData(username=username, user_id=user_id)
        return token_data
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or token expired")


# 转换hash密码
def get_password_hash(password: str) -> str:
    if not password:
        raise ValueError('密码不能为空!')
    return generate_password_hash(password)


# 验证密码
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return check_password_hash(hashed_password, plain_password)


# 验证是否为当前用户
async def current_user(token: str = Depends(oauth2), db: AsyncSession = Depends(get_db)) -> Admins:
    token_data = await verify_token(token)
    stmt = select(Admins).where(Admins.id == token_data.user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None or user.is_delete:
        raise HTTPException(status_code=401, detail="用户不存在或已被删除")
    return user

