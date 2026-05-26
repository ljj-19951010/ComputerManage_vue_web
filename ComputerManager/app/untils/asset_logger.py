#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project : app
@File    : asset_logger.py
@IDE     : PyCharm
@Author  : Jinjing
@Date    : 2026/5/20 17:10
@Desc    : 日志记录
"""
from datetime import date, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from models import AssetLogs


def serialize_value(value):
    """
    序列化值
    :param value:
    :return:
    """
    if isinstance(value, dict):         # 将字典转换json
        return {k: serialize_value(v) for k, v in value.items()}
    elif isinstance(value, list):           # 将列表转换json
        return [serialize_value(v) for v in value]
    elif isinstance(value, (datetime, date)):       # 将日期时间转换字符串
        return value.isoformat()
    else:
        return value


async def log_asset_operation(
        db: AsyncSession,
        asset_type: str,        # 电脑还是显示器类型
        asset_id: int,
        action: str,            # 操作类型 增删改查
        operator_id: int,           # 操作人id
        operator_type: str,             # 操作人类型，是管理员还是普通用户
        old_value: dict = None,         # 旧值
        new_value: dict = None,         # 新值
        remark: str = None          # 备注
):
    """
    记录资产操作日志
    :return:
    """
    # 序列化处理
    if old_value:
        old_value = serialize_value(old_value)
    if new_value:
        new_value = serialize_value(new_value)

    log_entry = AssetLogs(
        asset_type=asset_type,
        asset_id=asset_id,
        action=action,
        operator_id=operator_id,
        operator_type=operator_type,
        old_value=old_value,
        new_value=new_value,
        remark=remark
    )
    db.add(log_entry)
    await db.flush()            # 不用commit 等待外层统一提交
