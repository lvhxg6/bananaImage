"""
Gemini API 服务封装
使用 google-genai 库，支持自定义 API 端点
"""

import base64
import logging
from typing import Optional
from dataclasses import dataclass

from google import genai
from google.genai import types

from ..config import settings

logger = logging.getLogger(__name__)


@dataclass
class StyleTransferResult:
    """风格迁移结果"""
    success: bool
    image_data: Optional[bytes] = None
    description: Optional[str] = None
    error: Optional[str] = None


class GeminiService:
    """Gemini API 服务类"""

    def __init__(self):
        """初始化 Gemini 客户端"""
        self.client = None
        self._initialized = False

    def _ensure_initialized(self):
        """确保客户端已初始化"""
        if not self._initialized:
            if not settings.GEMINI_API_KEY:
                raise ValueError(
                    "GEMINI_API_KEY 未配置！\n"
                    "请在 .env 文件中设置或通过环境变量配置。"
                )

            # 根据官方示例配置客户端
            client_options = {
                "api_key": settings.GEMINI_API_KEY,
                "vertexai": True,  # 关键配置
            }

            # 如果有自定义 API 端点
            if settings.GEMINI_API_BASE:
                client_options["http_options"] = {
                    "base_url": settings.GEMINI_API_BASE
                }
                logger.info(f"使用自定义 API 端点: {settings.GEMINI_API_BASE}")

            self.client = genai.Client(**client_options)
            self._initialized = True
            logger.info("Gemini 客户端初始化成功")

    def _extract_result(self, response) -> StyleTransferResult:
        """从响应中提取结果"""
        import io
        image_data = None
        description = None

        try:
            # 记录响应结构用于调试
            logger.debug(f"响应类型: {type(response)}")
            logger.debug(f"响应属性: {dir(response)}")

            # google-genai 库的响应结构：response.candidates[0].content.parts
            parts = None

            # 方式1: 通过 candidates 访问
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts'):
                        parts = candidate.content.parts

            # 方式2: 直接访问 parts（某些版本可能支持）
            if parts is None and hasattr(response, 'parts'):
                parts = response.parts

            if parts is None:
                # 尝试获取文本响应
                if hasattr(response, 'text') and response.text:
                    return StyleTransferResult(
                        success=False,
                        description=response.text,
                        error="响应中未找到生成的图片，仅返回文本"
                    )
                return StyleTransferResult(
                    success=False,
                    error="无法解析响应结构"
                )

            # 遍历 parts 提取内容
            for part in parts:
                # 提取文本
                if hasattr(part, 'text') and part.text:
                    description = part.text
                    logger.debug(f"提取到文本: {description[:100] if description else 'None'}...")

                # 提取图片 - 方式1: inline_data
                if hasattr(part, 'inline_data') and part.inline_data:
                    inline_data = part.inline_data
                    if hasattr(inline_data, 'data') and inline_data.data:
                        image_data = inline_data.data
                        # 如果是 base64 编码的字符串，需要解码
                        if isinstance(image_data, str):
                            image_data = base64.b64decode(image_data)
                        logger.info(f"从 inline_data 提取到图片，大小: {len(image_data)} bytes")

                # 提取图片 - 方式2: 使用 PIL Image
                if image_data is None:
                    try:
                        # 某些版本的 SDK 支持直接转换为 PIL Image
                        if hasattr(part, 'to_image'):
                            image = part.to_image()
                        elif hasattr(part, 'as_image'):
                            image = part.as_image()
                        else:
                            image = None

                        if image:
                            buffer = io.BytesIO()
                            image.save(buffer, format='PNG')
                            image_data = buffer.getvalue()
                            logger.info(f"从 PIL Image 提取到图片，大小: {len(image_data)} bytes")
                    except Exception as img_err:
                        logger.debug(f"尝试提取 PIL Image 失败: {img_err}")

            if image_data:
                return StyleTransferResult(
                    success=True,
                    image_data=image_data,
                    description=description
                )
            else:
                return StyleTransferResult(
                    success=False,
                    description=description,
                    error="响应中未找到生成的图片"
                )

        except Exception as e:
            logger.error(f"解析响应失败: {e}", exc_info=True)
            return StyleTransferResult(
                success=False,
                error=f"解析响应失败: {str(e)}"
            )

    def style_transfer(
        self,
        content_image_bytes: bytes,
        style_image_bytes: bytes,
        prompt: Optional[str] = None,
        aspect_ratio: str = "1:1",
        resolution: str = "2K",
        output_format: str = "JPEG"
    ) -> StyleTransferResult:
        """
        执行风格迁移

        Args:
            content_image_bytes: 内容图片的字节数据
            style_image_bytes: 风格图片的字节数据
            prompt: 自定义提示词（可选）
            aspect_ratio: 输出图片的宽高比
            resolution: 输出图片的分辨率
            output_format: 输出图片的格式

        Returns:
            StyleTransferResult: 包含生成图片数据和描述的结果对象
        """
        try:
            self._ensure_initialized()

            # 使用默认提示词或自定义提示词
            final_prompt = prompt if prompt else settings.DEFAULT_STYLE_PROMPT

            # 构建请求内容
            contents = [
                final_prompt,
                types.Part.from_bytes(
                    data=content_image_bytes,
                    mime_type="image/jpeg"
                ),
                types.Part.from_bytes(
                    data=style_image_bytes,
                    mime_type="image/jpeg"
                )
            ]

            logger.info(
                f"开始风格迁移: aspect_ratio={aspect_ratio}, "
                f"resolution={resolution}, format={output_format}"
            )

            # 调用 API
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=contents
            )

            # 提取结果
            result = self._extract_result(response)

            if result.success:
                logger.info("风格迁移成功")
            else:
                logger.warning(f"风格迁移失败: {result.error}")

            return result

        except Exception as e:
            error_msg = str(e)
            logger.error(f"风格迁移异常: {error_msg}")

            # 处理特定错误
            if "RATE_LIMIT" in error_msg.upper() or "429" in error_msg:
                return StyleTransferResult(
                    success=False,
                    error="API 配额已用尽，请稍后再试"
                )
            elif "INVALID" in error_msg.upper():
                return StyleTransferResult(
                    success=False,
                    error="图片格式无效或损坏"
                )
            elif "API_KEY" in error_msg.upper() or "401" in error_msg:
                return StyleTransferResult(
                    success=False,
                    error="API Key 无效或未配置"
                )
            else:
                return StyleTransferResult(
                    success=False,
                    error=f"API 调用失败: {error_msg}"
                )

    def text_to_image(
        self,
        prompt: str,
        aspect_ratio: str = "1:1",
        resolution: str = "2K",
        output_format: str = "JPEG"
    ) -> StyleTransferResult:
        """
        文生图：根据文字描述生成图片

        Args:
            prompt: 图片描述文字
            aspect_ratio: 输出图片的宽高比
            resolution: 输出图片的分辨率
            output_format: 输出图片的格式

        Returns:
            StyleTransferResult: 包含生成图片数据和描述的结果对象
        """
        try:
            self._ensure_initialized()

            if not prompt or not prompt.strip():
                return StyleTransferResult(
                    success=False,
                    error="提示词不能为空"
                )

            logger.info(
                f"开始文生图: prompt={prompt[:50]}..., "
                f"aspect_ratio={aspect_ratio}, resolution={resolution}"
            )

            # 调用 API - 文生图只需要文字提示
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=[prompt]
            )

            # 提取结果
            result = self._extract_result(response)

            if result.success:
                logger.info("文生图成功")
            else:
                logger.warning(f"文生图失败: {result.error}")

            return result

        except Exception as e:
            error_msg = str(e)
            logger.error(f"文生图异常: {error_msg}")

            # 处理特定错误
            if "RATE_LIMIT" in error_msg.upper() or "429" in error_msg:
                return StyleTransferResult(
                    success=False,
                    error="API 配额已用尽，请稍后再试"
                )
            elif "API_KEY" in error_msg.upper() or "401" in error_msg:
                return StyleTransferResult(
                    success=False,
                    error="API Key 无效或未配置"
                )
            else:
                return StyleTransferResult(
                    success=False,
                    error=f"API 调用失败: {error_msg}"
                )

    def check_api_key(self) -> bool:
        """检查 API Key 是否有效"""
        try:
            self._ensure_initialized()
            return True
        except Exception:
            return False


# 创建全局服务实例
gemini_service = GeminiService()
