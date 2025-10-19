"""视频分析工具"""

from typing import Dict, Any, List
import requests

from ..core.config import get_settings
from ..core.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


class VideoAnalyzer:
    """视频内容分析器"""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Cookie": settings.bili_cookie or ""
        }
        self.api_base = "https://api.bilibili.com"
    
    def analyze_video(self, video: Dict[str, Any]) -> Dict[str, Any]:
        """分析视频内容
        
        Args:
            video: 视频数据
            
        Returns:
            分析结果
        """
        logger.info(f"分析视频: {video.get('bvid')}")
        
        bvid = video.get("bvid", "")
        
        try:
            # 获取视频详情
            detail = self._get_video_detail(bvid)
            
            # 提取关键信息
            insights = {
                "bvid": bvid,
                "title": video.get("title", ""),
                "description": video.get("description", ""),
                "tags": detail.get("tags", []),
                "duration": video.get("duration", 0),
                "stats": {
                    "view": detail.get("stat", {}).get("view", 0),
                    "like": detail.get("stat", {}).get("like", 0),
                    "coin": detail.get("stat", {}).get("coin", 0),
                    "favorite": detail.get("stat", {}).get("favorite", 0),
                    "share": detail.get("stat", {}).get("share", 0),
                },
                "author": video.get("author", ""),
                "pubdate": video.get("pubdate", 0)
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"视频分析失败: {str(e)}")
            return {}
    
    def analyze_comments(self, bvid: str, top_k: int = 50) -> Dict[str, Any]:
        """分析评论区
        
        Args:
            bvid: 视频BV号
            top_k: 获取前K条评论
            
        Returns:
            评论分析结果
        """
        logger.info(f"分析评论: {bvid}")
        
        try:
            comments = self._get_comments(bvid, top_k)
            
            if not comments:
                return {"total": 0, "comments": []}
            
            # 提取热门评论
            hot_comments = sorted(
                comments,
                key=lambda x: x.get("like", 0),
                reverse=True
            )[:10]
            
            analysis = {
                "total": len(comments),
                "hot_comments": [
                    {
                        "content": c.get("content", ""),
                        "like": c.get("like", 0),
                        "author": c.get("member", {}).get("uname", "")
                    }
                    for c in hot_comments
                ],
                "keywords": self._extract_keywords(comments)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"评论分析失败: {str(e)}")
            return {}
    
    def _get_video_detail(self, bvid: str) -> Dict[str, Any]:
        """获取视频详情
        
        Args:
            bvid: 视频BV号
            
        Returns:
            视频详情
        """
        url = f"{self.api_base}/x/web-interface/view"
        params = {"bvid": bvid}
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                return data.get("data", {})
            else:
                logger.warning(f"获取视频详情失败: {data.get('message')}")
                return {}
                
        except Exception as e:
            logger.error(f"请求失败: {str(e)}")
            return {}
    
    def _get_comments(self, bvid: str, limit: int) -> List[Dict[str, Any]]:
        """获取评论
        
        Args:
            bvid: 视频BV号
            limit: 评论数量限制
            
        Returns:
            评论列表
        """
        # 获取aid
        detail = self._get_video_detail(bvid)
        aid = detail.get("aid")
        
        if not aid:
            return []
        
        url = f"{self.api_base}/x/v2/reply"
        params = {
            "type": 1,
            "oid": aid,
            "sort": 2,  # 按热度排序
            "ps": min(limit, 20),
            "pn": 1
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                replies = data.get("data", {}).get("replies", [])
                return [
                    {
                        "content": r.get("content", {}).get("message", ""),
                        "like": r.get("like", 0),
                        "member": r.get("member", {})
                    }
                    for r in replies
                ]
            else:
                return []
                
        except Exception as e:
            logger.error(f"获取评论失败: {str(e)}")
            return []
    
    def _extract_keywords(self, comments: List[Dict[str, Any]]) -> List[str]:
        """从评论中提取关键词
        
        Args:
            comments: 评论列表
            
        Returns:
            关键词列表
        """
        # 简单实现：提取高频词
        from collections import Counter
        
        all_text = " ".join([c.get("content", "") for c in comments])
        words = all_text.split()
        
        # 过滤停用词和短词
        stop_words = {"的", "了", "是", "在", "我", "有", "和", "就", "不", "人", "都", "一"}
        filtered_words = [w for w in words if len(w) > 1 and w not in stop_words]
        
        # 统计频率
        counter = Counter(filtered_words)
        top_keywords = [word for word, count in counter.most_common(10)]
        
        return top_keywords

