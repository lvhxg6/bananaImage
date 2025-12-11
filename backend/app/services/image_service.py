"""
图片处理服务
提供图片验证、预处理、保存等功能
"""

import io
import uuid
import logging
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime

from PIL import Image, ExifTags

from ..config import settings

logger = logging.getLogger(__name__)


class ImageService:
    """图片处理服务类"""

    @staticmethod
    def validate_image(
        file_bytes: bytes,
        mime_type: str
    ) -> Tuple[bool, Optional[str]]:
        """
        验证图片有效性

        Args:
            file_bytes: 图片字节数据
            mime_type: MIME 类型

        Returns:
            (是否有效, 错误信息)
        """
        # 检查文件大小
        if len(file_bytes) > settings.MAX_IMAGE_SIZE:
            return False, f"图片大小超过限制 ({settings.MAX_IMAGE_SIZE // 1024 // 1024}MB)"

        # 检查 MIME 类型
        if mime_type not in settings.ALLOWED_MIME_TYPES:
            return False, f"不支持的图片格式: {mime_type}"

        # 尝试打开图片验证有效性
        try:
            img = Image.open(io.BytesIO(file_bytes))
            img.verify()
            return True, None
        except Exception as e:
            return False, f"图片文件损坏或无效: {str(e)}"

    @staticmethod
    def _fix_orientation(img: Image.Image) -> Image.Image:
        """根据 EXIF 信息修正图片方向"""
        try:
            # 获取 EXIF 中的方向标签
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break

            exif = img._getexif()
            if exif is not None:
                orientation_value = exif.get(orientation)
                if orientation_value == 3:
                    img = img.rotate(180, expand=True)
                elif orientation_value == 6:
                    img = img.rotate(270, expand=True)
                elif orientation_value == 8:
                    img = img.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            pass

        return img

    @staticmethod
    def process_image_for_api(
        image_bytes: bytes,
        max_dimension: int = None
    ) -> bytes:
        """
        预处理图片以供 API 使用

        - 自动旋转（根据 EXIF）
        - 尺寸限制
        - 格式转换为 JPEG
        - 压缩优化

        Args:
            image_bytes: 原始图片字节数据
            max_dimension: 最大尺寸（默认使用配置）

        Returns:
            处理后的图片字节数据
        """
        max_dim = max_dimension or settings.MAX_IMAGE_DIMENSION

        # 打开图片
        img = Image.open(io.BytesIO(image_bytes))

        # 修正方向
        img = ImageService._fix_orientation(img)

        # 转换为 RGB（去除 alpha 通道）
        if img.mode in ('RGBA', 'LA', 'P'):
            # 创建白色背景
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # 尺寸限制
        if max(img.size) > max_dim:
            img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
            logger.info(f"图片已缩小至 {img.size}")

        # 保存为 JPEG
        output = io.BytesIO()
        img.save(
            output,
            format='JPEG',
            quality=settings.COMPRESS_QUALITY,
            optimize=True
        )

        return output.getvalue()

    @staticmethod
    def save_result_image(
        image_data: bytes,
        output_format: str = "JPEG"
    ) -> Tuple[str, Path]:
        """
        保存生成的图片

        Args:
            image_data: 图片字节数据
            output_format: 输出格式

        Returns:
            (文件名, 文件路径)
        """
        # 确保输出目录存在
        settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # 生成唯一文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]
        extension = "jpg" if output_format.upper() == "JPEG" else output_format.lower()
        filename = f"style_transfer_{timestamp}_{unique_id}.{extension}"

        # 保存文件
        file_path = settings.OUTPUT_DIR / filename
        file_path.write_bytes(image_data)

        logger.info(f"图片已保存: {file_path}")

        return filename, file_path

    @staticmethod
    def get_image_info(image_bytes: bytes) -> dict:
        """
        获取图片信息

        Args:
            image_bytes: 图片字节数据

        Returns:
            包含图片信息的字典
        """
        try:
            img = Image.open(io.BytesIO(image_bytes))
            return {
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "mode": img.mode,
                "size_bytes": len(image_bytes)
            }
        except Exception as e:
            logger.error(f"获取图片信息失败: {e}")
            return {}

    @staticmethod
    def cleanup_old_files(max_age_hours: int = 24) -> int:
        """
        清理过期的临时文件

        Args:
            max_age_hours: 文件保留时间（小时）

        Returns:
            删除的文件数量
        """
        from datetime import timedelta

        deleted_count = 0
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)

        # 清理上传目录
        for file_path in settings.UPLOAD_DIR.glob("*"):
            if file_path.is_file():
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_time:
                    file_path.unlink()
                    deleted_count += 1

        # 清理输出目录
        for file_path in settings.OUTPUT_DIR.glob("*"):
            if file_path.is_file() and file_path.name != ".gitkeep":
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_time:
                    file_path.unlink()
                    deleted_count += 1

        if deleted_count > 0:
            logger.info(f"清理了 {deleted_count} 个过期文件")

        return deleted_count


# 创建全局服务实例
image_service = ImageService()
