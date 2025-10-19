"""Flask + FastHTML应用主文件"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from fasthtml.common import *
from datetime import datetime
import uuid

from .components import (
    page_layout,
    navbar,
    hero_section,
    task_card,
    create_modal,
    stats_section,
    loading_spinner,
    alert
)
from ..agent.graph import create_agent_graph, run_agent
from ..core.config import get_settings
from ..core.logger import setup_logger, get_logger

# 初始化配置和日志
settings = get_settings()
logger = setup_logger(
    name="videoagent",
    log_file=settings.logs_dir / "app.log"
)

# 创建Flask应用
flask_app = Flask(__name__)
CORS(flask_app)

# 创建Agent图
agent_graph = create_agent_graph()

# 任务存储（实际应用中应使用数据库）
tasks_store = {}


def create_app():
    """创建并配置应用"""
    
    # ========== FastHTML路由 ==========
    
    @flask_app.route("/")
    def index():
        """首页"""
        content = [
            navbar(),
            hero_section(),
            create_modal(),
            
            # 统计区域
            Div(
                H2("任务统计", cls="text-3xl font-bold mb-4"),
                Div(id="stats_section", hx_get="/api/stats", hx_trigger="load, every 5s"),
                cls="container mx-auto p-4"
            ),
            
            # 任务列表
            Div(
                H2("任务列表", cls="text-3xl font-bold mb-4"),
                Div(
                    id="task_list",
                    hx_get="/api/tasks",
                    hx_trigger="load, every 10s",
                    cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
                ),
                cls="container mx-auto p-4"
            )
        ]
        
        html = page_layout("VideoAgent - AI视频创作助手", *content)
        return to_xml(html)
    
    # ========== API路由 ==========
    
    @flask_app.route("/api/tasks", methods=["GET"])
    def get_tasks():
        """获取任务列表"""
        try:
            # 按创建时间倒序
            sorted_tasks = sorted(
                tasks_store.values(),
                key=lambda x: x.get("created_at", datetime.min),
                reverse=True
            )
            
            # 返回前20个
            tasks = sorted_tasks[:20]
            
            # 生成任务卡片HTML
            cards = [task_card(task) for task in tasks]
            
            if not cards:
                return to_xml(Div(
                    P("暂无任务", cls="text-center text-base-content/50 py-8"),
                ))
            
            return to_xml(Group(*cards))
            
        except Exception as e:
            logger.error(f"获取任务列表失败: {str(e)}")
            return to_xml(alert(f"加载失败: {str(e)}", "error"))
    
    @flask_app.route("/api/tasks", methods=["POST"])
    def create_task():
        """创建新任务"""
        try:
            # 获取表单数据
            task_type = request.form.get("task_type", "complete")
            keywords_str = request.form.get("keywords", "")
            user_input = request.form.get("user_input", "")
            
            # 解析关键词
            keywords = [k.strip() for k in keywords_str.split(",") if k.strip()]
            
            if not keywords:
                keywords = ["AI", "科技"]
            
            # 创建任务ID
            task_id = str(uuid.uuid4())
            
            # 初始化任务
            task = {
                "id": task_id,
                "title": f"任务 - {', '.join(keywords[:3])}",
                "description": user_input or "自动生成视频",
                "status": "pending",
                "task_type": task_type,
                "keywords": keywords,
                "user_input": user_input,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "result": None,
                "error": None
            }
            
            tasks_store[task_id] = task
            
            # 异步执行任务（这里简化为同步）
            try:
                task["status"] = "running"
                task["updated_at"] = datetime.now()
                
                # 运行Agent
                result = run_agent(
                    agent_graph,
                    user_input=user_input,
                    task_type=task_type,
                    task_id=task_id,
                    keywords=keywords
                )
                
                task["status"] = "completed" if result.get("completed") else "failed"
                task["result"] = result
                task["error"] = result.get("error")
                task["updated_at"] = datetime.now()
                
            except Exception as e:
                logger.error(f"任务执行失败: {str(e)}")
                task["status"] = "failed"
                task["error"] = str(e)
                task["updated_at"] = datetime.now()
            
            # 返回新任务卡片
            return to_xml(task_card(task))
            
        except Exception as e:
            logger.error(f"创建任务失败: {str(e)}")
            return to_xml(alert(f"创建失败: {str(e)}", "error"))
    
    @flask_app.route("/api/tasks/<task_id>", methods=["GET"])
    def get_task(task_id: str):
        """获取任务详情"""
        task = tasks_store.get(task_id)
        
        if not task:
            return jsonify({"error": "任务不存在"}), 404
        
        return jsonify(task)
    
    @flask_app.route("/api/stats", methods=["GET"])
    def get_stats():
        """获取统计信息"""
        try:
            stats = {
                "total": len(tasks_store),
                "pending": sum(1 for t in tasks_store.values() if t["status"] == "pending"),
                "running": sum(1 for t in tasks_store.values() if t["status"] == "running"),
                "completed": sum(1 for t in tasks_store.values() if t["status"] == "completed"),
                "failed": sum(1 for t in tasks_store.values() if t["status"] == "failed")
            }
            
            return to_xml(stats_section(stats))
            
        except Exception as e:
            logger.error(f"获取统计失败: {str(e)}")
            return to_xml(alert(f"加载失败: {str(e)}", "error"))
    
    @flask_app.route("/health", methods=["GET"])
    def health():
        """健康检查"""
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat()
        })
    
    return flask_app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host=settings.api_host,
        port=settings.api_port,
        debug=settings.debug
    )

