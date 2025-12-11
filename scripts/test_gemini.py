#!/usr/bin/env python3
"""
Gemini API 测试脚本
用于测试 API Key 是否有效，以及基本的图片生成功能
"""

import os
import sys
from pathlib import Path

# 添加 backend 到 Python 路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv

# 加载环境变量
env_path = backend_path / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    print(f"警告: .env 文件不存在: {env_path}")
    print("请复制 .env.example 为 .env 并配置 GEMINI_API_KEY")


def test_api_key():
    """测试 API Key 是否有效"""
    print("\n=== 测试 Gemini API Key ===\n")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("❌ GEMINI_API_KEY 未配置")
        print("\n请在 .env 文件中设置 GEMINI_API_KEY")
        print("申请地址: https://aistudio.google.com/app/apikey")
        return False

    if api_key == "your_api_key_here":
        print("❌ GEMINI_API_KEY 未修改为真实的 API Key")
        print("\n请将 .env 文件中的 GEMINI_API_KEY 修改为您的真实 API Key")
        return False

    print(f"✓ API Key 已配置: {api_key[:8]}...{api_key[-4:]}")

    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        print("✓ Gemini 客户端创建成功")

        # 尝试列出可用模型
        print("\n正在检查可用模型...")
        # 简单的验证方式：尝试生成一个简单的文本
        response = client.models.generate_content(
            model="gemini-2.0-flash",  # 使用更通用的模型测试
            contents="Hello, respond with just 'OK'"
        )

        if response and response.text:
            print("✓ API 调用成功")
            print(f"  响应: {response.text[:50]}...")
            return True
        else:
            print("❌ API 调用返回空响应")
            return False

    except Exception as e:
        print(f"❌ API 验证失败: {e}")
        return False


def test_image_generation():
    """测试图片生成功能"""
    print("\n=== 测试图片生成功能 ===\n")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("跳过: API Key 未正确配置")
        return False

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        print("正在测试 gemini-3-pro-image-preview 模型...")
        print("(这可能需要 15-30 秒)")

        # 测试简单的文本到图片生成
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents="Generate a simple blue square image",
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"]
            )
        )

        if response and response.candidates:
            print("✓ 图片生成 API 调用成功")

            # 检查是否有图片数据
            for candidate in response.candidates:
                for part in candidate.content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        print("✓ 成功接收到图片数据")
                        return True
                    if hasattr(part, 'text') and part.text:
                        print(f"  文本响应: {part.text[:100]}...")

            print("⚠ 响应中未找到图片数据")
            return False
        else:
            print("❌ API 调用返回空响应")
            return False

    except Exception as e:
        error_msg = str(e)
        print(f"❌ 图片生成测试失败: {error_msg}")

        if "not found" in error_msg.lower() or "does not exist" in error_msg.lower():
            print("\n提示: gemini-3-pro-image-preview 模型可能不可用")
            print("请检查您的 API 配额和模型访问权限")

        return False


def main():
    """主函数"""
    print("=" * 50)
    print("Gemini API 测试工具")
    print("=" * 50)

    # 测试 API Key
    api_key_valid = test_api_key()

    # 如果 API Key 有效，测试图片生成
    if api_key_valid:
        print("\n" + "-" * 50)
        test_image_generation()

    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)

    # 使用说明
    if not api_key_valid:
        print("\n下一步:")
        print("1. 访问 https://aistudio.google.com/app/apikey 申请 API Key")
        print("2. 复制 backend/.env.example 为 backend/.env")
        print("3. 在 .env 文件中设置 GEMINI_API_KEY=你的API密钥")
        print("4. 重新运行此测试脚本")


if __name__ == "__main__":
    main()
