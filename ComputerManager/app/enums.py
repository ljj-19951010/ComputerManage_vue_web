#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project : app
@File    : enum.py
@IDE     : PyCharm
@Author  : Jinjing
@Date    : 2026/5/20 17:17
@Desc    :
枚举模块
定义一组符号名称（常量）来代表固定的可选值。它可以大幅提升代码的可读性、可维护性和安全性。
解决魔法数字或者注释问题
比如：stats=1 的1什么意思 或者 男/女 0/1等问题，可以集中管理
"""
from enum import Enum, IntEnum


# 枚举
class UserStatusEnum(IntEnum):
    """
    员工状态
    """
    WORK = 1          # 在职
    NOTWORK = 0           # 离职


class AssetTypeEnum(str, Enum):
    """
    类型
    """
    COMPUTER = 'computer'
    MONITOR = 'monitor'
    EMPLOYEE = 'employee'
    USER = 'user'


class OperatorTypeEnum(str, Enum):
    """
    操作员类型
    """
    ADMIN = 'admin'
    USER = 'user'


class ActionEnum(str, Enum):
    """
    操作类型
    """
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
    ASSIGN = 'assign'
    RECLAIM = 'reclaim'
    REPAIR = 'repair'
    RETIRE = 'retire'


class ComputersStatus(str, Enum):
    AVAILABLE = 'available'
    IN_USE = 'in_use'
    REPAIR = 'repair'
    RETIRED = 'retired'
    DELETED = 'deleted'


class MonitorsStatus(str, Enum):
    AVAILABLE = 'available'
    IN_USE = 'in_use'
    REPAIR = 'repair'
    RETIRED = 'retired'
    DELETED = 'deleted'


class ModelsCategory(str, Enum):
    COMPUTER = 'computer'
    MONITOR = 'monitor'
