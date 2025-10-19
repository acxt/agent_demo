"""Agent工作流节点实现"""

from typing import Dict, Any
from datetime import datetime

from .state import AgentState
from ..tools.hotspot import HotspotFinder
from ..tools.analyzer import VideoAnalyzer
from ..tools.generator import PromptGenerator, VideoGenerator
from ..core.config import get_settings
from ..core.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


def route_task(state: AgentState) -> AgentState:
    """路由任务类型
    
    Args:
        state: 当前状态
        
    Returns:
        更新后的状态
    """
    logger.info(f"路由任务: {state.get('task_type', 'unknown')}")
    
    state["current_step"] = "routing"
    state["updated_at"] = datetime.now()
    state["messages"].append(f"开始处理任务: {state.get('user_input', '')}")
    
    return state


def find_hotspots(state: AgentState) -> AgentState:
    """查找热点视频
    
    Args:
        state: 当前状态
        
    Returns:
        更新后的状态
    """
    logger.info("开始查找热点视频")
    state["current_step"] = "finding_hotspots"
    
    try:
        finder = HotspotFinder()
        keywords = state.get("keywords", [])
        
        if not keywords:
            keywords = ["AI", "科技"]  # 默认关键词
        
        hotspots = finder.find_hotspots(keywords, top_k=10)
        
        state["hotspot_videos"] = hotspots
        state["selected_video"] = hotspots[0] if hotspots else None
        state["messages"].append(f"找到 {len(hotspots)} 个热点视频")
        
    except Exception as e:
        logger.error(f"热点查找失败: {str(e)}")
        state["error"] = str(e)
        state["messages"].append(f"热点查找失败: {str(e)}")
    
    state["updated_at"] = datetime.now()
    return state


def analyze_video(state: AgentState) -> AgentState:
    """分析视频内容
    
    Args:
        state: 当前状态
        
    Returns:
        更新后的状态
    """
    logger.info("开始分析视频")
    state["current_step"] = "analyzing"
    
    try:
        analyzer = VideoAnalyzer()
        video = state.get("selected_video")
        
        if not video:
            raise ValueError("没有选中的视频")
        
        # 分析视频
        insights = analyzer.analyze_video(video)
        comments = analyzer.analyze_comments(video.get("bvid", ""))
        
        state["video_insights"] = insights
        state["comments_analysis"] = comments
        state["messages"].append("视频分析完成")
        
    except Exception as e:
        logger.error(f"视频分析失败: {str(e)}")
        state["error"] = str(e)
        state["messages"].append(f"视频分析失败: {str(e)}")
    
    state["updated_at"] = datetime.now()
    return state


def generate_prompt(state: AgentState) -> AgentState:
    """生成视频提示词
    
    Args:
        state: 当前状态
        
    Returns:
        更新后的状态
    """
    logger.info("开始生成提示词")
    state["current_step"] = "generating_prompt"
    
    try:
        generator = PromptGenerator()
        
        insights = state.get("video_insights", {})
        comments = state.get("comments_analysis", {})
        
        # 生成提示词
        prompt_result = generator.generate_prompt(
            video_insights=insights,
            comments_analysis=comments,
            user_input=state.get("user_input", "")
        )
        
        state["prompt_text"] = prompt_result.get("text", "")
        state["prompt_json"] = prompt_result.get("json", {})
        state["messages"].append("提示词生成完成")
        
    except Exception as e:
        logger.error(f"提示词生成失败: {str(e)}")
        state["error"] = str(e)
        state["messages"].append(f"提示词生成失败: {str(e)}")
    
    state["updated_at"] = datetime.now()
    return state


def create_video(state: AgentState) -> AgentState:
    """创建视频
    
    Args:
        state: 当前状态
        
    Returns:
        更新后的状态
    """
    logger.info("开始创建视频")
    state["current_step"] = "creating_video"
    
    try:
        generator = VideoGenerator()
        
        prompt_text = state.get("prompt_text", "")
        if not prompt_text:
            raise ValueError("没有提示词")
        
        # 生成视频
        video_url = generator.generate_video(prompt_text)
        
        state["video_url"] = video_url
        state["messages"].append("视频创建完成")
        
    except Exception as e:
        logger.error(f"视频创建失败: {str(e)}")
        state["error"] = str(e)
        state["messages"].append(f"视频创建失败: {str(e)}")
    
    state["updated_at"] = datetime.now()
    return state


def format_output(state: AgentState) -> AgentState:
    """格式化输出结果
    
    Args:
        state: 当前状态
        
    Returns:
        更新后的状态
    """
    logger.info("格式化输出结果")
    state["current_step"] = "completed"
    state["completed"] = True
    state["updated_at"] = datetime.now()
    
    if not state.get("error"):
        state["messages"].append("所有任务完成")
    
    return state

