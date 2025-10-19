# API 文档

## 基础信息

- **Base URL**: `http://127.0.0.1:8000`
- **Content-Type**: `application/json` 或 `application/x-www-form-urlencoded`

## 端点列表

### 1. 健康检查

```http
GET /health
```

**响应示例**:

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
}
```

### 2. 获取任务列表

```http
GET /api/tasks
```

**响应**: HTML 片段（用于 HTMX）

### 3. 创建任务

```http
POST /api/tasks
Content-Type: application/x-www-form-urlencoded
```

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| task_type | string | 否 | 任务类型: complete/hotspot/analyze/generate |
| keywords | string | 否 | 搜索关键词，逗号分隔 |
| user_input | string | 否 | 用户需求描述 |

**请求示例**:

```
task_type=complete&keywords=AI,科技&user_input=创作一个AI教程视频
```

**响应**: HTML 任务卡片

### 4. 获取任务详情

```http
GET /api/tasks/{task_id}
```

**响应示例**:

```json
{
  "id": "uuid",
  "title": "任务标题",
  "status": "completed",
  "task_type": "complete",
  "keywords": ["AI", "科技"],
  "created_at": "2024-01-01T12:00:00",
  "result": {
    "video_url": "https://...",
    "prompt": "..."
  }
}
```

### 5. 获取统计信息

```http
GET /api/stats
```

**响应**: HTML 统计组件

## 任务状态

- `pending`: 等待执行
- `running`: 执行中
- `completed`: 已完成
- `failed`: 执行失败

## 任务类型

- `complete`: 完整流程（热点 → 分析 → 生成 → 视频）
- `hotspot`: 仅查找热点
- `analyze`: 分析指定视频
- `generate`: 生成提示词

## 错误处理

所有错误会返回适当的 HTTP 状态码和错误信息。

**错误响应示例**:

```json
{
  "error": "错误描述"
}
```

## 使用示例

### cURL

```bash
# 创建任务
curl -X POST http://127.0.0.1:8000/api/tasks \
  -d "task_type=complete" \
  -d "keywords=AI,机器学习" \
  -d "user_input=创作一个机器学习入门视频"

# 查询任务
curl http://127.0.0.1:8000/api/tasks/{task_id}
```

### Python

```python
import requests

# 创建任务
response = requests.post(
    "http://127.0.0.1:8000/api/tasks",
    data={
        "task_type": "complete",
        "keywords": "AI,科技",
        "user_input": "创作一个科普视频"
    }
)

# 查询任务
task_id = "..."
response = requests.get(f"http://127.0.0.1:8000/api/tasks/{task_id}")
print(response.json())
```
