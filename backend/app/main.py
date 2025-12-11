"""
FastAPI 应用入口
风格迁移 Web 服务主程序
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings, ensure_directories
from .api.style_transfer import router as style_transfer_router

# 配置日志
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("正在启动服务...")
    ensure_directories()

    if settings.GEMINI_API_KEY:
        logger.info("Gemini API Key 已配置")
    else:
        logger.warning(
            "警告: GEMINI_API_KEY 未配置！\n"
            "请在 .env 文件中设置或通过环境变量配置。\n"
            "申请地址: https://aistudio.google.com/app/apikey"
        )

    logger.info(f"服务启动完成，监听 {settings.HOST}:{settings.PORT}")

    yield

    # 关闭时执行
    logger.info("服务正在关闭...")


# 创建 FastAPI 应用
app = FastAPI(
    title="Gemini 风格迁移 API",
    description="""
    基于 Google Gemini 3 Pro Image 模型的图片风格迁移服务。

    ## 功能特点

    - **风格迁移**: 将一张图片的艺术风格应用到另一张图片上
    - **多种分辨率**: 支持 1K/2K/4K 输出
    - **多种宽高比**: 支持 1:1, 16:9, 9:16 等多种比例
    - **高质量输出**: 基于 Gemini 3 Pro Image 模型

    ## 使用方法

    1. 上传内容图片（提供图像内容结构）
    2. 上传风格图片（提供艺术风格）
    3. 选择输出参数（分辨率、宽高比等）
    4. 获取生成的风格迁移图片
    """,
    version="1.0.0",
    lifespan=lifespan
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(style_transfer_router)


@app.get("/")
async def root():
    """根路径，返回欢迎信息"""
    return {
        "message": "欢迎使用 Gemini 风格迁移 API",
        "docs": "/docs",
        "health": "/api/health",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
