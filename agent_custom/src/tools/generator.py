"""内容生成工具"""

from typing import Dict, Any, Optional
import json

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

from ..core.config import get_settings
from ..core.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


class PromptGenerator:
    """提示词生成器"""
    
    def __init__(self):
        api_keys = settings.get_gemini_keys()
        if not api_keys:
            raise ValueError("未配置Gemini API密钥")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=api_keys[0],
            temperature=0.7
        )
    
    def generate_prompt(
        self,
        video_insights: Dict[str, Any],
        comments_analysis: Dict[str, Any],
        user_input: str = ""
    ) -> Dict[str, Any]:
        """生成视频提示词
        
        Args:
            video_insights: 视频分析结果
            comments_analysis: 评论分析结果
            user_input: 用户输入
            
        Returns:
            生成的提示词（文本和JSON格式）
        """
        logger.info("开始生成提示词")
        
        try:
            # 构建提示
            system_prompt = """你是一个专业的视频创意专家。
根据提供的视频数据和评论分析，生成一个吸引人的短视频提示词。

要求：
1. 提示词要简洁、生动、具有画面感
2. 长度控制在200字以内
3. 融合热点元素和用户需求
4. 输出纯文本描述，不要包含任何标签或格式"""
            
            user_message = f"""
视频信息：
- 标题：{video_insights.get('title', '')}
- 描述：{video_insights.get('description', '')}
- 标签：{', '.join(video_insights.get('tags', [])[:5])}

热门评论关键词：{', '.join(comments_analysis.get('keywords', [])[:10])}

用户需求：{user_input or '创作一个有趣的短视频'}

请生成视频提示词：
"""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message)
            ]
            
            response = self.llm.invoke(messages)
            prompt_text = response.content.strip()
            
            # 构建JSON格式
            prompt_json = {
                "prompt": prompt_text,
                "style": "realistic",
                "duration": 5,
                "aspect_ratio": "16:9",
                "metadata": {
                    "source_video": video_insights.get('bvid', ''),
                    "keywords": comments_analysis.get('keywords', [])[:5]
                }
            }
            
            logger.info("提示词生成成功")
            
            return {
                "text": prompt_text,
                "json": prompt_json
            }
            
        except Exception as e:
            logger.error(f"提示词生成失败: {str(e)}")
            raise


class VideoGenerator:
    """视频生成器"""
    
    def __init__(self):
        self.api_key = settings.veo_api_key
        if not self.api_key:
            logger.warning("未配置VEO API密钥，将使用模拟模式")
    
    def generate_video(self, prompt: str) -> str:
        """生成视频
        
        Args:
            prompt: 视频提示词
            
        Returns:
            视频URL
        """
        logger.info("开始生成视频")
        
        try:
            if not self.api_key:
                # 模拟模式
                logger.info("模拟视频生成")
                return f"https://example.com/videos/mock_{hash(prompt)}.mp4"
            
            # TODO: 集成真实的VEO API
            # 这里需要根据实际API文档实现
            
            logger.info("视频生成成功")
            return "https://example.com/videos/generated.mp4"
            
        except Exception as e:
            logger.error(f"视频生成失败: {str(e)}")
            raise

