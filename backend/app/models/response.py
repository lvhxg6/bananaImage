"""
响应模型定义
"""

from typing import Optional
from pydantic import BaseModel, Field


class ImageMetadata(BaseModel):
    """图片元数据"""

    aspect_ratio: str = Field(description="宽高比")
    resolution: str = Field(description="分辨率")
    output_format: str = Field(description="输出格式")
    processing_time: float = Field(description="处理时间(秒)")
    width: Optional[int] = Field(default=None, description="图片宽度")
    height: Optional[int] = Field(default=None, description="图片高度")


class StyleTransferResponse(BaseModel):
    """风格迁移响应"""

    success: bool = Field(description="是否成功")
    image_url: Optional[str] = Field(default=None, description="生成图片的URL")
    description: Optional[str] = Field(default=None, description="Gemini 返回的描述")
    metadata: Optional[ImageMetadata] = Field(default=None, description="图片元数据")
    error: Optional[str] = Field(default=None, description="错误信息")


class ConfigResponse(BaseModel):
    """配置选项响应"""

    aspect_ratios: list[str] = Field(description="可用的宽高比选项")
    resolutions: list[str] = Field(description="可用的分辨率选项")
    output_formats: list[str] = Field(description="可用的输出格式")
    max_image_size: int = Field(description="最大图片大小(字节)")
    allowed_mime_types: list[str] = Field(description="允许的图片类型")
    default_prompt: str = Field(description="默认提示词")


class HealthResponse(BaseModel):
    """健康检查响应"""

    status: str = Field(description="服务状态")
    api_key_configured: bool = Field(description="API Key 是否已配置")
    version: str = Field(default="1.0.0", description="服务版本")
