#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project : app
@File    : database.py
@IDE     : PyCharm
@Author  : Jinjing
@Date    : 2026/5/19 17:17
@Desc    :
数据库配置
会话管理
模型基类
"""
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from config import settings


# 创建模型基类
class Base(DeclarativeBase):
    """
    所有ORM模型基类
    """
    pass


# 创建引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,         # 是否打印SQL语句
    future=True,            # 使用异步的SQLAlchemy

    # pool_pre_ping=True,          # 连接池中的连接在每次使用之前都会被检查，以确保它们仍然有效
    pool_size=settings.DB_POOL_SIZE,          # 连接池大小
    max_overflow=settings.DB_MAX_OVERFLOW,          # 连接池溢出大小
    pool_timeout=settings.DB_POOL_TIMEOUT,          # 连接池超时时间
    pool_recycle=settings.DB_POOL_RECYCLE,          # 连接池回收时间
    connect_args={
        "charset": "utf8mb4",
        "use_unicode": True,        # 使用Unicode编码
    }
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,          # 会话在提交后不会立即关闭，而是在下一次使用时才关闭
    class_=AsyncSession,
    autoflush=False,          # 在会话中执行查询之前不会自动刷新会话
    autocommit=False          # 在会话中执行查询之前不会自动提交会话
)


# 获取数据库会话
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    每个请求都会创建一个数据库会话
    :return:  用完会自动关闭
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            raise
        except Exception:
            await session.rollback()
            raise


# 关闭数据库连接
async def close_db():
    """
    关闭数据库连接
    :return:
    """
    await engine.dispose()
