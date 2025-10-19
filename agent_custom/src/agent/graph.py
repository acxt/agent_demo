"""Agent工作流图定义"""

from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

from .state import AgentState
from .nodes import (
    route_task,
    find_hotspots,
    analyze_video,
    generate_prompt,
    create_video,
    format_output
)
from ..core.logger import get_logger

logger = get_logger(__name__)


def create_agent_graph() -> StateGraph:
    """创建Agent工作流图
    
    Returns:
        配置好的StateGraph实例
    """
    # 创建状态图
    workflow = StateGraph(AgentState)
    
    # 添加节点
    workflow.add_node("route", route_task)
    workflow.add_node("find_hotspots", find_hotspots)
    workflow.add_node("analyze", analyze_video)
    workflow.add_node("generate", generate_prompt)
    workflow.add_node("create", create_video)
    workflow.add_node("format", format_output)
    
    # 设置入口点
    workflow.set_entry_point("route")
    
    # 添加条件边：根据任务类型路由
    workflow.add_conditional_edges(
        "route",
        lambda x: x.get("task_type", "complete"),
        {
            "hotspot": "find_hotspots",
            "analyze": "analyze",
            "generate": "generate",
            "complete": "format",
        }
    )
    
    # 热点发现 -> 分析
    workflow.add_edge("find_hotspots", "analyze")
    
    # 分析 -> 生成
    workflow.add_edge("analyze", "generate")
    
    # 生成 -> 创建视频
    workflow.add_edge("generate", "create")
    
    # 创建视频 -> 格式化输出
    workflow.add_edge("create", "format")
    
    # 格式化输出 -> 结束
    workflow.add_edge("format", END)
    
    # 编译图
    app = workflow.compile()
    
    logger.info("Agent工作流图创建成功")
    return app


def run_agent(
    graph: StateGraph,
    user_input: str,
    task_type: str = "complete",
    **kwargs
) -> Dict[str, Any]:
    """运行Agent
    
    Args:
        graph: 编译后的工作流图
        user_input: 用户输入
        task_type: 任务类型
        **kwargs: 其他参数
        
    Returns:
        执行结果
    """
    from datetime import datetime
    
    # 初始化状态
    initial_state: AgentState = {
        "task_id": kwargs.get("task_id", f"task_{datetime.now().timestamp()}"),
        "task_type": task_type,
        "user_input": user_input,
        "keywords": kwargs.get("keywords", []),
        "current_step": "start",
        "completed": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "messages": [],
        "metadata": {}
    }
    
    try:
        # 执行工作流
        result = graph.invoke(initial_state)
        logger.info(f"任务 {initial_state['task_id']} 执行完成")
        return result
        
    except Exception as e:
        logger.error(f"任务执行失败: {str(e)}", exc_info=True)
        return {
            **initial_state,
            "error": str(e),
            "completed": False
        }

