# 使用指南

## 快速开始

### 1. 启动应用

```bash
# Windows
.\run.ps1

# Linux/Mac
./run.sh

# 或直接运行
python main.py
```

应用将在 http://127.0.0.1:8000 启动

### 2. 创建第一个任务

1. 打开浏览器访问 http://127.0.0.1:8000
2. 点击"开始创作"按钮
3. 填写表单：
   - **任务类型**: 选择"完整流程"
   - **关键词**: 输入"AI, 科技"
   - **创作需求**: 描述想要的视频内容
4. 点击"创建"按钮

### 3. 查看任务进度

任务卡片会自动刷新显示状态：

- 🟡 **pending**: 等待执行
- 🔵 **running**: 执行中
- 🟢 **completed**: 已完成
- 🔴 **failed**: 执行失败

## 功能详解

### 热点发现

从 B 站抓取指定关键词的热门视频，基于以下指标排序：

- 播放量
- 点赞数
- 评论数
- 弹幕数
- 时间衰减

**示例**:

```python
keywords = ["AI", "机器学习", "深度学习"]
# 将返回最近7天内的热门视频
```

### 视频分析

深度分析选中的视频：

- 视频元数据（标题、描述、标签）
- 统计数据（播放、点赞、收藏等）
- 评论区分析
- 关键词提取

### 提示词生成

使用 Gemini AI 根据视频分析结果生成视频创作提示词：

- 融合热点元素
- 结合用户需求
- 生成简洁生动的描述
- 输出 JSON 格式

**生成示例**:

```json
{
  "prompt": "一个展示AI技术应用的短视频...",
  "style": "realistic",
  "duration": 5,
  "aspect_ratio": "16:9"
}
```

### 视频生成

调用 VEO API 生成视频（需要配置 API 密钥）

## 任务类型

### 完整流程 (complete)

执行所有步骤：热点发现 → 分析 → 生成提示词 → 创建视频

### 仅查找热点 (hotspot)

只执行热点发现步骤，返回热门视频列表

### 分析视频 (analyze)

分析指定视频的内容和评论

### 生成提示词 (generate)

根据分析结果生成视频提示词

## 高级用法

### 通过 API 调用

```python
import requests

# 创建任务
response = requests.post(
    "http://127.0.0.1:8000/api/tasks",
    data={
        "task_type": "complete",
        "keywords": "Python,教程",
        "user_input": "创作一个Python入门教程视频"
    }
)

# 查询任务
task_id = response.json()["id"]
status = requests.get(f"http://127.0.0.1:8000/api/tasks/{task_id}")
print(status.json())
```

### 自定义配置

编辑 `config/settings.yaml`:

```yaml
hotspot:
  lookback_days: 14 # 增加回溯天数
  top_k: 20 # 返回更多结果

llm:
  temperature: 0.8 # 增加创意度
```

## 常见问题

### Q: 任务一直处于 pending 状态

A: 检查 API 密钥配置，查看 logs 目录下的日志文件

### Q: 无法获取 B 站数据

A: 需要配置有效的 BILI_COOKIE

### Q: 视频生成失败

A: VEO API 需要单独申请，未配置时为模拟模式

### Q: 如何查看详细日志

A: 日志文件位于 `logs/app.log`

## 最佳实践

1. **关键词选择**: 使用 2-5 个相关关键词
2. **需求描述**: 描述清晰具体
3. **定期清理**: 使用 `make clean` 清理缓存
4. **监控日志**: 出现问题时查看日志文件
5. **API 限流**: 注意第三方 API 的调用限制

## 性能优化

- 使用代理提高 B 站 API 访问速度
- 配置多个 Gemini API 密钥实现负载均衡
- 开启 Redis 缓存热点数据
- 使用数据库持久化任务状态
