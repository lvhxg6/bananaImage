# Gemini 风格迁移 Web 应用

基于 Google Gemini 3 Pro Image 模型的图片风格迁移应用。上传两张图片（内容图 + 风格图），生成融合了内容和风格的新图片。

## 功能特点

- **风格迁移**: 将一张图片的艺术风格应用到另一张图片上
- **多种分辨率**: 支持 1K/2K/4K 输出
- **多种宽高比**: 支持 1:1, 16:9, 9:16, 4:3, 3:4 等
- **Web 界面**: 友好的图片上传和预览界面
- **实时处理**: 显示处理进度和预计时间

## 环境要求

- Python 3.11+
- Node.js 18.0+
- Gemini API Key ([申请地址](https://aistudio.google.com/app/apikey))

## 快速开始

### 1. 配置 API Key

```bash
cd backend
cp .env.example .env
# 编辑 .env 文件，设置 GEMINI_API_KEY
```

### 2. 启动后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000/docs 查看 API 文档

### 3. 启动前端

```bash
cd frontend
npm install
npm start
```

访问 http://localhost:3000

## 测试 API

```bash
python scripts/test_gemini.py
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/style-transfer` | POST | 提交风格迁移任务 |
| `/api/outputs/{filename}` | GET | 下载生成的图片 |
| `/api/config` | GET | 获取配置选项 |
| `/api/health` | GET | 健康检查 |

### 风格迁移请求示例

```bash
curl -X POST "http://localhost:8000/api/style-transfer" \
  -F "content_image=@content.jpg" \
  -F "style_image=@style.jpg" \
  -F "aspect_ratio=1:1" \
  -F "resolution=2K"
```

## 项目结构

```
.
├── backend/                  # FastAPI 后端
│   ├── app/
│   │   ├── main.py          # 应用入口
│   │   ├── config.py        # 配置管理
│   │   ├── models/          # 数据模型
│   │   ├── services/        # 业务逻辑
│   │   └── api/             # API 路由
│   ├── uploads/             # 上传目录
│   ├── outputs/             # 输出目录
│   └── requirements.txt
│
├── frontend/                # React 前端
│   └── src/
│       ├── components/      # 组件
│       └── services/        # API 调用
│
├── scripts/                 # 工具脚本
│   └── test_gemini.py      # API 测试
│
└── README.md
```

## 技术栈

- **后端**: FastAPI + Python
- **前端**: React + TailwindCSS
- **AI 模型**: Google Gemini 3 Pro Image
- **图片处理**: Pillow

## 许可证

MIT License
