#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project : app
@File    : config.py
@IDE     : PyCharm
@Author  : Jinjing
@Date    : 2026/5/19 17:17
@Desc    : 设置连接配置文件
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30           # 过期时间
    DB_ECHO: bool = False           # 是否打印sql
    DB_POOL_SIZE: int = 10       # 连接池大小
    DB_MAX_OVERFLOW: int = 20           # 连接池溢出大小
    DB_POOL_TIMEOUT: int = 30           # 连接池超时时间
    DB_POOL_RECYCLE: int = 3600         # 连接池回收时间

    class Config:
        env_file = ".env"           # 必须在根目录
        env_file_encoding = "utf-8"


settings = Settings()
