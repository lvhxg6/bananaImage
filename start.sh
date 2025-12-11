#!/bin/bash

# Gemini 风格迁移应用一键启动脚本
# macOS / Linux

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "  Gemini 风格迁移应用启动脚本"
echo "========================================"
echo ""

# 检查 .env 文件
if [ ! -f "backend/.env" ]; then
    echo "⚠ 未找到 backend/.env 文件"
    echo "  正在从模板创建..."
    cp backend/.env.example backend/.env
    echo "  请编辑 backend/.env 文件，设置 GEMINI_API_KEY"
    echo ""
fi

# 启动后端
echo "📦 启动后端服务..."
cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "  创建 Python 虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "  安装 Python 依赖..."
pip install -q -r requirements.txt

# 启动后端服务
echo "  启动 FastAPI 服务..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cd "$SCRIPT_DIR"

# 等待后端启动
sleep 3

# 启动前端
echo ""
echo "🎨 启动前端服务..."
cd frontend

# 检查 .env 文件
if [ ! -f ".env" ]; then
    cp .env.example .env
fi

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo "  安装前端依赖（首次运行可能需要几分钟）..."
    npm install
fi

# 启动前端服务
echo "  启动 React 开发服务器..."
npm start &
FRONTEND_PID=$!

cd "$SCRIPT_DIR"

echo ""
echo "========================================"
echo "  服务启动成功！"
echo "========================================"
echo ""
echo "  🌐 前端地址: http://localhost:3000"
echo "  📡 后端地址: http://localhost:8000"
echo "  📚 API 文档: http://localhost:8000/docs"
echo ""
echo "  按 Ctrl+C 停止所有服务"
echo ""

# 等待中断信号
trap "echo ''; echo '正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

wait
