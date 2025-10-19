"""Agent状态定义"""

from typing import TypedDict, Optional, List, Dict, Any
from datetime import datetime


class AgentState(TypedDict, total=False):
    """Agent执行状态"""
    
    # 任务信息
    task_id: str
    task_type: str  # hotspot, analyze, generate, complete
    user_input: str
    
    # 热点数据
    keywords: List[str]
    hotspot_videos: List[Dict[str, Any]]
    selected_video: Optional[Dict[str, Any]]
    
    # 分析结果
    video_insights: Optional[Dict[str, Any]]
    comments_analysis: Optional[Dict[str, Any]]
    
    # 生成内容
    prompt_text: str
    prompt_json: Optional[Dict[str, Any]]
    video_url: Optional[str]
    
    # 执行状态
    current_step: str
    error: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
    
    # 中间结果
    messages: List[str]
    metadata: Dict[str, Any]

