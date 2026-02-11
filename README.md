# Yudao FastAPI Mini (Monorepo)

本项目是基于 [yudao-boot-mini](https://gitee.com/zhijiantianya/yudao-boot-mini) 的重构版本，采用了现代化的前后端分离架构和 Monorepo 管理模式。

后端迁移至 **Python (FastAPI)**，前端保持 **Vue3 + Element Plus**，旨在提供一个轻量、高效的全栈开发框架。

## 🏗 项目结构

```text
.
├── backend/            # 后端服务 (Python + FastAPI)
│   ├── app/            # 应用代码
│   ├── sql/            # SQL 脚本
│   └── scripts/        # 工具脚本
├── frontend/           # 前端应用 (Vue3 + Vite)
├── manage.py           # 项目管理脚本 (入口)
└── README.md
```

## 🚀 快速开始

### 1. 环境准备

确保你的本地环境已安装：
*   **Python**: 3.14+
*   **Node.js**: 18+
*   **UV**: Python 极速包管理器（推荐 `pip install uv`）

### 2. 安装依赖

在项目根目录下，使用 `manage.py` 一键安装前后端所有依赖：

```bash
python manage.py install
```
> 该命令会自动执行后端的 `uv sync` 和前端的 `npm install`。

### 3. 初始化数据库

确保你已经配置好 PostgreSQL 数据库，并在 `backend/.env` 中正确设置了数据库连接字符串。然后运行：

```bash
python manage.py init-db
```

### 4. 启动开发环境

一键并发启动前端（Vue）和后端（FastAPI）服务：

```bash
python manage.py dev
```

启动成功后，访问：
*   **前端**: [http://localhost:5173](http://localhost:5173) (视具体端口而定)
*   **后端文档**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🛠 常用命令

所有任务均通过根目录下的 `manage.py` 管理：

| 任务 | 命令 | 说明 |
| :--- | :--- | :--- |
| **安装依赖** | `python manage.py install` | 安装前后端依赖 |
| **初始化DB** | `python manage.py init-db` | 执行 SQL 初始化脚本 |
| **启动全栈** | `python manage.py dev` | 并行启动前后端开发服务 |
| **仅后端** | `python manage.py dev:backend` | 单独启动 FastAPI (带热重载) |
| **仅前端** | `python manage.py dev:frontend` | 单独启动 Vite 开发服务 |
| **构建发布** | `python manage.py build` | 构建前端生产代码 |

## 📦 部署参考

### 后端部署
```bash
cd backend
# 使用 uv 或 pip 安装依赖
uv sync
# 启动生产服务
.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
```

### 前端部署
```bash
cd frontend
npm run build:prod
# 构建产物位于 frontend/dist，可使用 Nginx 部署
```

## 📝 贡献与开发

*   **Python 规范**: 遵循 PEP8，建议使用 Ruff 进行 Lint。
*   **前端规范**: 遵循 ESLint + Prettier。
*   **Git 提交**: 推荐使用 Conventional Commits 规范。
