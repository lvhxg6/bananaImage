"""
请求模型定义
"""

from typing import Optional
from pydantic import BaseModel, Field


class StyleTransferRequest(BaseModel):
    """风格迁移请求参数"""

    prompt: Optional[str] = Field(
        default=None,
        description="自定义提示词，描述如何进行风格迁移"
    )

    aspect_ratio: str = Field(
        default="1:1",
        description="输出图片的宽高比",
        examples=["1:1", "16:9", "9:16", "4:3", "3:4"]
    )

    resolution: str = Field(
        default="2K",
        description="输出图片的分辨率",
        examples=["1K", "2K", "4K"]
    )

    output_format: str = Field(
        default="JPEG",
        description="输出图片的格式",
        examples=["JPEG", "PNG"]
    )
