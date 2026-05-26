import logging
from contextlib import asynccontextmanager
from urllib.request import Request

from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from database import close_db, engine
from router import employee, computers, monitors
from router.admin import users

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 检查数据库连接
async def check_db_health() -> bool:
    """
    检查数据库连接
    :return: True or False
    """
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"check_db_health error:{type(e).__name__} {e}")
        return False


# 生命周期
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动
    logger.info("start...")
    # 启动时检查数据库连接
    if not await check_db_health():
        logger.error("Database connection failed")
        raise RuntimeError("数据库连接失败")
    logger.info("数据库连接成功")
    # 这里可以加载其他资源比如redis
    yield
    # 关闭
    logger.info("shut down...")
    await close_db()
    # 这里可以释放其他资源比如redis
    logger.info("关闭成功")


# 创建应用
app = FastAPI(
    lifespan=lifespan,
    title="资产管理",
    description="资产管理API",
    version="0.0.1"
)

# 配置cors
app.add_middleware(
    CORSMiddleware,         # 跨域
    allow_origins=["*"],            # 允许所有域名
    allow_credentials=True,         # 允许cookie
    allow_methods=["*"],            # 允许所有请求方法
    allow_headers=["*"]         # 允许所有请求头
)


# 全局异常处理
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc:SQLAlchemyError):
    logger.error(f"SQLAlchemyError: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error: 数据库连接异常!"}
    )

app.include_router(users.router)            # 后台用户管理
app.include_router(employee.router)            # 员工管理
app.include_router(computers.router)            # 电脑管理
app.include_router(monitors.router)         # 显示器管理


# 健康检查断点(负载均衡器或监控使用)
@app.get("/health")
async def health_check():
    if await check_db_health():
        return {"status": "good"}
    else:
        return JSONResponse(status_code=503, content={"status": "unavailable"})


# 全局异常处理
@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    if 'Duplicate entry' in str(exc):
        return JSONResponse(status_code=400, content={"detail": "数据重复违反唯一约束"})
    return JSONResponse(status_code=400, content={"detail": "数据完整性错误"})
