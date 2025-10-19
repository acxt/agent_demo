# VideoAgent - AI视频创作助手

基于热点分析的智能视频生成系统，使用 Flask + FastHTML + DaisyUI + LangGraph 构建。

## 功能特点

- 🔥 **热点发现**：自动从B站抓取热门视频
- 📊 **智能分析**：深度分析视频内容和评论
- ✨ **提示词生成**：AI生成视频创作提示词
- 🎬 **视频生成**：集成VEO API生成视频
- 🎨 **现代UI**：FastHTML + DaisyUI响应式界面
- 🔄 **工作流管理**：LangGraph状态机管理

## 技术栈

- **后端框架**：Flask 3.0
- **UI框架**：FastHTML + DaisyUI
- **AI框架**：LangChain + LangGraph
- **LLM**：Google Gemini
- **视频生成**：Google Veo

## 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `env_example.txt` 为 `.env` 并填写配置：

```env
DEEPSEEK_API_KEY=your_key
GEMINI_API_KEYS=key1,key2,key3
VEO_API_KEY=your_key
BILI_COOKIE=your_cookie
```

### 3. 运行应用

```bash
python main.py
```

访问 http://127.0.0.1:8000

## 项目结构

```
agent_custom/
├── src/
│   ├── agent/              # Agent核心
│   │   ├── state.py        # 状态定义
│   │   ├── graph.py        # 工作流图
│   │   └── nodes.py        # 节点实现
│   ├── core/               # 核心模块
│   │   ├── config.py       # 配置管理
│   │   └── logger.py       # 日志管理
│   ├── tools/              # 工具集
│   │   ├── hotspot.py      # 热点发现
│   │   ├── analyzer.py     # 视频分析
│   │   └── generator.py    # 内容生成
│   └── ui/                 # UI界面
│       ├── app.py          # Flask应用
│       └── components.py   # FastHTML组件
├── config/                 # 配置文件
├── data/                   # 数据目录
├── logs/                   # 日志目录
├── main.py                 # 入口文件
└── requirements.txt        # 依赖列表
```

## API文档

### 创建任务

```bash
POST /api/tasks
Content-Type: application/x-www-form-urlencoded

task_type=complete&keywords=AI,科技&user_input=创作一个科普视频
```

### 查询任务

```bash
GET /api/tasks
GET /api/tasks/{task_id}
```

### 获取统计

```bash
GET /api/stats
```

## 开发指南

### 添加新工具

在 `src/tools/` 目录创建新工具类，并在 `__init__.py` 中导出。

### 自定义工作流

修改 `src/agent/graph.py` 中的节点和边定义。

### UI组件开发

在 `src/ui/components.py` 中使用 FastHTML + DaisyUI 创建组件。

## 许可证

MIT License

