#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project : app
@File    : schemas.py
@IDE     : PyCharm
@Author  : Jinjing
@Date    : 2026/5/19 17:16
@Desc    : 
"""
from datetime import datetime
from typing import Optional, TypeVar, Generic, List

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from enums import UserStatusEnum, ComputersStatus, MonitorsStatus

T = TypeVar('T')


class Page(BaseModel, Generic[T]):
    """
    分页模型
    """
    total: int
    data: List[T]


# token schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None


# admins schemas
class ShowAdmins(BaseModel):
    username: str
    email: str
    is_supper: bool
    is_active: bool
    is_delete: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CreateAdmins(BaseModel):
    username: str
    password: str
    email: EmailStr
    is_supper: bool = False
    is_active: Optional[bool] = True
    is_delete: Optional[bool] = False
    created_at: datetime = Field(default_factory=datetime.now)


class UpdateAdmins(BaseModel):
    password: Optional[str] = None
    email: Optional[str] = None
    is_supper: Optional[bool] = None
    is_active: Optional[bool] = None
    is_delete: Optional[bool] = None
    updated_at: datetime = Field(default_factory=datetime.now)


# users schemas
class ShowUsers(BaseModel):
    id: int
    name: str
    english_name: str
    email: str
    computer_tags: Optional[list] = []
    status: UserStatusEnum          # 在职状态或离职状态
    department_id: Optional[int] = None
    department_name: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UpdateUsers(BaseModel):
    name: Optional[str] = None
    english_name: Optional[str] = None
    email: Optional[str] = None
    status: Optional[UserStatusEnum] = None
    department_id: Optional[int] = None
    updated_at: datetime = Field(default_factory=datetime.now)


class CreateUser(BaseModel):
    name: str
    english_name: str
    email: EmailStr
    status: Optional[UserStatusEnum] = UserStatusEnum.WORK
    department_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)


# computers schemas
class ShowComputers(BaseModel):
    asset_tag: str          # 资产编号
    serial_number: str          # 序列号
    model_id: int           # 型号ID
    status: Optional[ComputersStatus] = ComputersStatus.AVAILABLE          # 状态
    employee_id: Optional[int] = None
    employee_name: Optional[str] = None
    price: Optional[str] = None         # 价格
    remark: Optional[str] = None         # 备注
    purchase_date: Optional[datetime] = None             # 购买日期
    deleted_at: Optional[datetime] = None             # 删除时间
    model_config = ConfigDict(from_attributes=True)


class CreateComputers(BaseModel):
    asset_tag: str          # 资产编号
    serial_number: str          # 序列号
    model_id: int           # 型号ID
    status: ComputersStatus = ComputersStatus.AVAILABLE          # 状态
    employee_id: Optional[int] = None
    employee_name: Optional[str] = None
    price: Optional[str] = None         # 价格
    remark: Optional[str] = None         # 备注
    purchase_date: datetime = Field(default_factory=datetime.now)             # 购买日期
    warranty_end: datetime = None             # 保修结束日期


class UpdateComputers(BaseModel):
    status: Optional[ComputersStatus] = None          # 状态
    employee_id: Optional[int] = None
    employee_name: Optional[str] = None
    remark: Optional[str] = None         # 备注


# monitors schemas
class ShowMonitors(BaseModel):
    asset_tag: str          # 资产编号
    serial_number: str          # 序列号
    model_id: int           # 型号ID
    employee_id: Optional[int] = None
    employee_name: Optional[str] = None
    status: MonitorsStatus = MonitorsStatus.AVAILABLE           # 状态
    price: Optional[str] = None
    remark: Optional[str] = None          # 备注
    purchase_date: Optional[datetime] = None         # 购买日期
    deleted_at: Optional[datetime] = None         # 删除时间
    model_config = ConfigDict(from_attributes=True)


class CreateMonitors(BaseModel):
    asset_tag: str          # 资产编号
    serial_number: str          # 序列号
    model_id: int           # 型号ID
    employee_id: Optional[int] = None
    employee_name: Optional[str] = None
    status: MonitorsStatus = MonitorsStatus.AVAILABLE           # 状态
    price: str
    remark: Optional[str] = None         # 备注
    purchase_date: datetime         # 购买日期
    warranty_end: datetime = None             # 保修结束日期


class UpdateMonitors(BaseModel):
    status: Optional[MonitorsStatus] = None          # 状态
    employee_id: Optional[int] = None
    employee_name: Optional[str] = None
    remark: Optional[str] = None         # 备注


# departments schemas