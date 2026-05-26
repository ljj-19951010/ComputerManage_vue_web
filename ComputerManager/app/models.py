from typing import Optional, List
import datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKeyConstraint, Index, JSON, String, text, Text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from enums import AssetTypeEnum, OperatorTypeEnum, ComputersStatus, ModelsCategory, MonitorsStatus


class Admins(Base):
    __tablename__ = 'admins'
    __table_args__ = (
        Index('uk_username', 'username', unique=True),
        {'comment': '用户表'}
    )

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, comment='用户ID')
    username: Mapped[str] = mapped_column(String(50, 'utf8mb4_unicode_ci'), nullable=False, comment='账号')
    password_hash: Mapped[str] = mapped_column(String(255, 'utf8mb4_unicode_ci'), nullable=False, comment='bcrypt密码哈希')
    email: Mapped[str] = mapped_column(String(200, 'utf8mb4_unicode_ci'), nullable=False, comment='邮箱')
    is_supper: Mapped[int] = mapped_column(TINYINT, nullable=False, server_default=text("'0'"), comment='角色:1管理员0普通用户')
    is_active: Mapped[int] = mapped_column(TINYINT, nullable=False, server_default=text("'1'"), comment='是否激活 默认1')
    is_delete: Mapped[int] = mapped_column(TINYINT, nullable=False, server_default=text("'0'"),comment='是否被删除 默认0')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    last_login_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='最后登录时间')


class AssetLogs(Base):
    __tablename__ = 'asset_logs'
    __table_args__ = (
        Index('idx_asset', 'asset_type', 'asset_id'),
        Index('idx_created_at', 'created_at'),
        Index('idx_operator', 'operator_id', 'operator_type'),
        {'comment': '资产操作日志表'}
    )

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True)
    asset_type: Mapped[AssetTypeEnum] = mapped_column(Enum(AssetTypeEnum, values_callable=lambda cls: [member.value for member in cls]), nullable=False, comment='资产类型')
    asset_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False, comment='资产ID')
    action: Mapped[str] = mapped_column(String(50, 'utf8mb4_unicode_ci'), nullable=False, comment='操作类型：assign/reclaim/repair/retire/update/create/delete')
    operator_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False, comment='操作人ID')
    operator_type: Mapped[OperatorTypeEnum] = mapped_column(Enum(OperatorTypeEnum, values_callable=lambda cls: [member.value for member in cls]), nullable=False, comment='操作人类型')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    old_value: Mapped[Optional[dict]] = mapped_column(JSON, comment='变更前的关键字段（如user_id, status）')
    new_value: Mapped[Optional[dict]] = mapped_column(JSON, comment='变更后的关键字段')
    remark: Mapped[Optional[str]] = mapped_column(String(500, 'utf8mb4_unicode_ci'), comment='备注')


class Brands(Base):
    __tablename__ = 'brands'
    __table_args__ = (
        Index('uk_name', 'name', unique=True),
        {'comment': '品牌表'}
    )

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(50, 'utf8mb4_unicode_ci'), nullable=False, comment='品牌名称')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    models: Mapped[list['Models']] = relationship('Models', back_populates='brand')


class Departments(Base):
    __tablename__ = 'departments'
    __table_args__ = (
        Index('idx_deleted_at', 'deleted_at'),
        Index('idx_status', 'status'),
        Index('uk_name', 'name', unique=True),
        {'comment': '科室表'}
    )

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, comment='科室ID')
    name: Mapped[str] = mapped_column(String(100, 'utf8mb4_unicode_ci'), nullable=False, comment='科室名称')
    status: Mapped[int] = mapped_column(TINYINT, nullable=False, server_default=text("'1'"), comment='状态：1-启用，0-停用')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间')
    email: Mapped[Optional[str]] = mapped_column(String(100, 'utf8mb4_unicode_ci'), comment='科室邮箱')
    remark: Mapped[Optional[str]] = mapped_column(String(200, 'utf8mb4_unicode_ci'), comment='备注')
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='软删除时间')

    users: Mapped[list['Users']] = relationship('Users', back_populates='department')


class Models(Base):
    __tablename__ = 'models'
    __table_args__ = (
        ForeignKeyConstraint(['brand_id'], ['brands.id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_model_brand'),
        Index('uk_brand_model_category', 'brand_id', 'name', 'category', unique=True),
        {'comment': '型号表'}
    )

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
    brand_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False, comment='品牌ID')
    name: Mapped[str] = mapped_column(String(100, 'utf8mb4_unicode_ci'), nullable=False, comment='型号名称')
    category: Mapped[ModelsCategory] = mapped_column(Enum(ModelsCategory, values_callable=lambda cls: [member.value for member in cls]), nullable=False, comment='适用设备类型')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    brand: Mapped['Brands'] = relationship('Brands', back_populates='models')
    computers: Mapped[list['Computers']] = relationship('Computers', back_populates='model')
    monitors: Mapped[list['Monitors']] = relationship('Monitors', back_populates='model')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        ForeignKeyConstraint(['department_id'], ['departments.id'], ondelete='SET NULL', onupdate='CASCADE', name='fk_user_department'),
        Index('idx_deleted_at', 'deleted_at'),
        Index('idx_department_id', 'department_id'),
        Index('idx_status', 'status'),
        Index('uk_email', 'email', unique=True),
        Index('uk_name', 'name', unique=True),
        {'comment': '员工表'}
    )

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, comment='用户ID')
    name: Mapped[str] = mapped_column(String(50, 'utf8mb4_unicode_ci'), nullable=False, comment='姓名')
    email: Mapped[str] = mapped_column(String(100, 'utf8mb4_unicode_ci'), nullable=False, comment='邮箱')
    status: Mapped[int] = mapped_column(TINYINT, nullable=False, server_default=text("'1'"), comment='状态：1-在职，0-离职')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='入职时间')
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    english_name: Mapped[Optional[str]] = mapped_column(String(200, 'utf8mb4_unicode_ci'), comment='英文名')
    department_id: Mapped[Optional[int]] = mapped_column(INTEGER(unsigned=True), comment='所属科室ID')
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='软删除时间(离职时间)')

    department: Mapped[Optional['Departments']] = relationship('Departments', back_populates='users')
    computers: Mapped[list['Computers']] = relationship('Computers', back_populates='user')
    monitors: Mapped[list['Monitors']] = relationship('Monitors', back_populates='user')

    # 加上这个可以让pydantic模型的字段 对应这个函数名，返回需要的显示的名称
    @property
    def department_name(self) -> str:
        return self.department.name if self.department else None

    @property
    def computer_tags(self) -> List[str]:
        return [t.asset_tag for t in self.computers] if self.computers else []


class Computers(Base):
    __tablename__ = 'computers'
    __table_args__ = (
        ForeignKeyConstraint(['model_id'], ['models.id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_computer_model'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL', onupdate='CASCADE', name='fk_computer_user'),
        Index('idx_deleted_at', 'deleted_at'),
        Index('idx_model_id', 'model_id'),
        Index('idx_status', 'status'),
        Index('idx_user_id', 'user_id'),
        Index('uk_asset_tag', 'asset_tag', unique=True),
        Index('uk_serial_number', 'serial_number', unique=True),
        {'comment': '电脑资产表'}
    )

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
    asset_tag: Mapped[str] = mapped_column(String(50, 'utf8mb4_unicode_ci'), nullable=False, comment='资产编号')
    serial_number: Mapped[str] = mapped_column(String(100, 'utf8mb4_unicode_ci'), nullable=False, comment='序列号')
    model_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False, comment='型号ID')
    status: Mapped[ComputersStatus] = mapped_column(Enum(ComputersStatus, values_callable=lambda cls: [member.value for member in cls]), nullable=False, server_default=text("'available'"), comment='状态')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    user_id: Mapped[Optional[int]] = mapped_column(INTEGER(unsigned=True), comment='当前使用者ID')
    price: Mapped[Optional[str]] = mapped_column(String(100, 'utf8mb4_unicode_ci'), comment='单价')
    assigned_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='最近分配时间')
    purchase_date: Mapped[Optional[datetime.date]] = mapped_column(Date, comment='购买日期')
    warranty_end: Mapped[Optional[datetime.date]] = mapped_column(Date, comment='保修截止')
    remark: Mapped[Optional[str]] = mapped_column(String(200, 'utf8mb4_unicode_ci'), comment='备注')
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='软删除时间')

    model: Mapped['Models'] = relationship('Models', back_populates='computers')
    user: Mapped[Optional['Users']] = relationship('Users', back_populates='computers')

    @property
    def employee_name(self) -> str:
        return self.user.name if self.user else None

    @property
    def employee_id(self) -> int:
        return self.user.id if self.user else None


class Monitors(Base):
    __tablename__ = 'monitors'
    __table_args__ = (
        ForeignKeyConstraint(['model_id'], ['models.id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_monitor_model'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL', onupdate='CASCADE', name='fk_monitor_user'),
        Index('idx_deleted_at', 'deleted_at'),
        Index('idx_model_id', 'model_id'),
        Index('idx_status', 'status'),
        Index('idx_user_id', 'user_id'),
        Index('uk_asset_tag', 'asset_tag', unique=True),
        Index('uk_serial_number', 'serial_number', unique=True),
        {'comment': '显示器资产表'}
    )

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
    asset_tag: Mapped[str] = mapped_column(String(50, 'utf8mb4_unicode_ci'), nullable=False, comment='资产编号')
    serial_number: Mapped[str] = mapped_column(String(100, 'utf8mb4_unicode_ci'), nullable=False, comment='序列号')
    model_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False, comment='型号ID')
    status: Mapped[MonitorsStatus] = mapped_column(Enum(MonitorsStatus, values_callable=lambda cls: [member.value for member in cls]), nullable=False, server_default=text("'available'"), comment='状态')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    user_id: Mapped[Optional[int]] = mapped_column(INTEGER(unsigned=True), comment='当前使用者ID')
    price: Mapped[Optional[str]] = mapped_column(String(100, 'utf8mb4_unicode_ci'), comment='单价')
    assigned_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='最近分配时间')
    purchase_date: Mapped[Optional[datetime.date]] = mapped_column(Date, comment='购买日期')
    warranty_end: Mapped[Optional[datetime.date]] = mapped_column(Date, comment='保修截止')
    remark: Mapped[Optional[str]] = mapped_column(String(200, 'utf8mb4_unicode_ci'), comment='备注')
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='软删除时间')

    model: Mapped['Models'] = relationship('Models', back_populates='monitors')
    user: Mapped[Optional['Users']] = relationship('Users', back_populates='monitors')

    @property
    def employee_name(self) -> str:
        return self.user.name if self.user else None

    @property
    def employee_id(self) -> int:
        return self.user.id if self.user else None
