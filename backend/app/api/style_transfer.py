"""
风格迁移 API 路由
提供图片上传、风格迁移、结果下载等接口
"""

import time
import logging
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse

from ..config import settings
from ..models.request import StyleTransferRequest
from ..models.response import (
    StyleTransferResponse,
    ConfigResponse,
    HealthResponse,
    ImageMetadata
)
from ..services.gemini_service import gemini_service
from ..services.image_service import image_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Style Transfer"])


@router.post("/style-transfer", response_model=StyleTransferResponse)
async def style_transfer(
    content_image: UploadFile = File(..., description="内容图片"),
    style_image: UploadFile = File(..., description="风格图片"),
    prompt: Optional[str] = Form(default=None, description="自定义提示词"),
    aspect_ratio: str = Form(default="1:1", description="宽高比"),
    resolution: str = Form(default="2K", description="分辨率"),
    output_format: str = Form(default="JPEG", description="输出格式")
):
    """
    执行风格迁移

    - **content_image**: 内容图片（提供图像内容结构）
    - **style_image**: 风格图片（提供艺术风格）
    - **prompt**: 可选的自定义提示词
    - **aspect_ratio**: 输出图片宽高比 (1:1, 16:9, 9:16, 4:3, 3:4)
    - **resolution**: 输出分辨率 (1K, 2K, 4K)
    - **output_format**: 输出格式 (JPEG, PNG)
    """
    start_time = time.time()

    try:
        # 验证参数
        if aspect_ratio not in settings.ASPECT_RATIOS:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的宽高比: {aspect_ratio}。可选: {settings.ASPECT_RATIOS}"
            )

        if resolution not in settings.RESOLUTIONS:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的分辨率: {resolution}。可选: {settings.RESOLUTIONS}"
            )

        if output_format.upper() not in settings.OUTPUT_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的输出格式: {output_format}。可选: {settings.OUTPUT_FORMATS}"
            )

        # 读取上传的图片
        content_bytes = await content_image.read()
        style_bytes = await style_image.read()

        # 验证内容图片
        is_valid, error = image_service.validate_image(
            content_bytes,
            content_image.content_type or "image/jpeg"
        )
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"内容图片无效: {error}")

        # 验证风格图片
        is_valid, error = image_service.validate_image(
            style_bytes,
            style_image.content_type or "image/jpeg"
        )
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"风格图片无效: {error}")

        # 预处理图片
        content_processed = image_service.process_image_for_api(content_bytes)
        style_processed = image_service.process_image_for_api(style_bytes)

        logger.info(
            f"开始风格迁移: content={len(content_processed)}B, "
            f"style={len(style_processed)}B"
        )

        # 调用 Gemini API 进行风格迁移
        result = gemini_service.style_transfer(
            content_image_bytes=content_processed,
            style_image_bytes=style_processed,
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            output_format=output_format.upper()
        )

        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)

        # 保存结果图片
        filename, file_path = image_service.save_result_image(
            result.image_data,
            output_format=output_format.upper()
        )

        # 获取生成图片的信息
        image_info = image_service.get_image_info(result.image_data)

        processing_time = time.time() - start_time

        return StyleTransferResponse(
            success=True,
            image_url=f"/api/outputs/{filename}",
            description=result.description,
            metadata=ImageMetadata(
                aspect_ratio=aspect_ratio,
                resolution=resolution,
                output_format=output_format.upper(),
                processing_time=round(processing_time, 2),
                width=image_info.get("width"),
                height=image_info.get("height")
            )
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"风格迁移失败: {e}")
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


@router.get("/outputs/{filename}")
async def get_output_image(filename: str):
    """获取生成的图片"""
    file_path = settings.OUTPUT_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="图片不存在")

    # 确定媒体类型
    media_type = "image/jpeg"
    if filename.lower().endswith(".png"):
        media_type = "image/png"

    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=filename
    )


@router.get("/config", response_model=ConfigResponse)
async def get_config():
    """获取可用的配置选项"""
    return ConfigResponse(
        aspect_ratios=settings.ASPECT_RATIOS,
        resolutions=settings.RESOLUTIONS,
        output_formats=settings.OUTPUT_FORMATS,
        max_image_size=settings.MAX_IMAGE_SIZE,
        allowed_mime_types=settings.ALLOWED_MIME_TYPES,
        default_prompt=settings.DEFAULT_STYLE_PROMPT
    )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查"""
    api_key_configured = gemini_service.check_api_key()

    return HealthResponse(
        status="healthy" if api_key_configured else "degraded",
        api_key_configured=api_key_configured,
        version="1.0.0"
    )


@router.post("/cleanup")
async def cleanup_files(max_age_hours: int = 24):
    """清理过期的临时文件"""
    deleted_count = image_service.cleanup_old_files(max_age_hours)
    return {"deleted_count": deleted_count, "max_age_hours": max_age_hours}
