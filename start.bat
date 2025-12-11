@echo off
chcp 65001 >nul
title Gemini 风格迁移应用

echo ========================================
echo   Gemini 风格迁移应用启动脚本
echo ========================================
echo.

cd /d %~dp0

REM 检查 .env 文件
if not exist "backend\.env" (
    echo ⚠ 未找到 backend\.env 文件
    echo   正在从模板创建...
    copy backend\.env.example backend\.env >nul
    echo   请编辑 backend\.env 文件，设置 GEMINI_API_KEY
    echo.
)

REM 启动后端
echo 📦 启动后端服务...
start "Backend" cmd /k "cd backend && if not exist venv (python -m venv venv) && venv\Scripts\activate && pip install -q -r requirements.txt && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM 等待后端启动
timeout /t 5 /nobreak >nul

REM 启动前端
echo.
echo 🎨 启动前端服务...

REM 检查 .env 文件
if not exist "frontend\.env" (
    copy frontend\.env.example frontend\.env >nul
)

start "Frontend" cmd /k "cd frontend && if not exist node_modules (npm install) && npm start"

echo.
echo ========================================
echo   服务启动中...
echo ========================================
echo.
echo   🌐 前端地址: http://localhost:3000
echo   📡 后端地址: http://localhost:8000
echo   📚 API 文档: http://localhost:8000/docs
echo.
echo   关闭此窗口不会停止服务
echo   如需停止，请手动关闭 Backend 和 Frontend 窗口
echo.

pause
