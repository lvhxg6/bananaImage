"""
配置管理模块
从环境变量加载配置，提供类型安全的配置访问
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 加载 .env 文件，override=True 确保 .env 文件优先于系统环境变量
load_dotenv(override=True)


class Settings(BaseSettings):
    """应用配置"""

    # Gemini API 配置 - 使用 load_dotenv 后的环境变量
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_API_BASE: str = os.getenv("GEMINI_API_BASE", "")
    GEMINI_MODEL: str = "gemini-3-pro-image-preview"

    # 文件路径配置
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    OUTPUT_DIR: Path = BASE_DIR / "outputs"

    # 图片处理配置
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024  # 10MB
    MAX_IMAGE_DIMENSION: int = 4096  # 最大尺寸
    COMPRESS_QUALITY: int = 85  # JPEG 压缩质量

    # 允许的图片格式
    ALLOWED_MIME_TYPES: list[str] = [
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/gif"
    ]

    # 图片生成配置选项
    ASPECT_RATIOS: list[str] = [
        "1:1", "16:9", "9:16", "4:3", "3:4",
        "3:2", "2:3", "21:9", "9:21"
    ]

    RESOLUTIONS: list[str] = ["1K", "2K", "4K"]

    OUTPUT_FORMATS: list[str] = ["JPEG", "PNG"]

    # 服务器配置
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # CORS 配置
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # 默认风格迁移提示词
    DEFAULT_STYLE_PROMPT: str = (
        "Transfer the artistic style from the second image to the first image. "
        "Keep the content structure of the first image while applying the visual style, "
        "colors, and artistic elements from the second image."
    )

    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()


def ensure_directories():
    """确保必要的目录存在"""
    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def validate_api_key():
    """验证 API Key 是否已配置"""
    if not settings.GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY 未配置！请在 .env 文件中设置或通过环境变量配置。\n"
            "申请地址: https://aistudio.google.com/app/apikey"
        )
    return True
