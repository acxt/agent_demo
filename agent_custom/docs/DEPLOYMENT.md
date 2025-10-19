# 部署指南

## 本地开发

### Windows

```powershell
# 1. 克隆项目
cd agent_demo\agent_custom

# 2. 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
copy env_example.txt .env
# 编辑.env文件填写API密钥

# 5. 启动应用
python main.py
# 或使用脚本
.\run.ps1
```

### Linux/Mac

```bash
# 1. 克隆项目
cd agent_demo/agent_custom

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp env_example.txt .env
# 编辑.env文件

# 5. 启动应用
python main.py
# 或使用脚本
chmod +x run.sh
./run.sh
```

## 生产部署

### 使用Gunicorn

```bash
# 安装Gunicorn
pip install gunicorn

# 启动服务
gunicorn -w 4 -b 0.0.0.0:8000 "src.ui.app:create_app()"
```

### 使用Docker

创建 `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "src.ui.app:create_app()"]
```

构建和运行:

```bash
docker build -t videoagent .
docker run -p 8000:8000 --env-file .env videoagent
```

### 使用Nginx反向代理

`nginx.conf`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 环境变量

必需配置:
- `GEMINI_API_KEYS`: Gemini API密钥（逗号分隔）
- `BILI_COOKIE`: B站Cookie

可选配置:
- `VEO_API_KEY`: VEO视频生成密钥
- `DEEPSEEK_API_KEY`: DeepSeek API密钥
- `API_HOST`: 服务器地址（默认127.0.0.1）
- `API_PORT`: 端口号（默认8000）

## 性能优化

1. **使用异步任务队列**（Celery/RQ）
2. **添加数据库**（PostgreSQL/MySQL）
3. **Redis缓存**
4. **CDN加速静态资源**
5. **负载均衡**（多实例）

## 监控

建议集成:
- **日志**: 使用日志聚合工具（ELK/Loki）
- **监控**: Prometheus + Grafana
- **错误追踪**: Sentry

## 备份

定期备份:
- 数据库
- 配置文件
- 生成的视频和提示词

