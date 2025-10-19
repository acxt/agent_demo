"""热点视频发现工具"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
import requests

from ..core.config import get_settings
from ..core.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


class HotspotFinder:
    """热点视频查找器"""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Cookie": settings.bili_cookie or ""
        }
        self.api_base = "https://api.bilibili.com"
    
    def find_hotspots(
        self,
        keywords: List[str],
        top_k: int = 10,
        lookback_days: int = 7
    ) -> List[Dict[str, Any]]:
        """查找热点视频
        
        Args:
            keywords: 搜索关键词列表
            top_k: 返回前K个结果
            lookback_days: 回溯天数
            
        Returns:
            热点视频列表
        """
        logger.info(f"开始查找热点: keywords={keywords}, top_k={top_k}")
        
        all_videos = []
        
        for keyword in keywords:
            try:
                videos = self._search_videos(keyword, lookback_days)
                all_videos.extend(videos)
            except Exception as e:
                logger.error(f"搜索关键词 '{keyword}' 失败: {str(e)}")
        
        # 去重和排序
        unique_videos = self._deduplicate_videos(all_videos)
        sorted_videos = self._rank_videos(unique_videos)
        
        return sorted_videos[:top_k]
    
    def _search_videos(self, keyword: str, days: int) -> List[Dict[str, Any]]:
        """搜索视频
        
        Args:
            keyword: 搜索关键词
            days: 回溯天数
            
        Returns:
            视频列表
        """
        url = f"{self.api_base}/x/web-interface/search/type"
        
        params = {
            "search_type": "video",
            "keyword": keyword,
            "order": "click",
            "duration": 0,
            "page": 1,
            "pagesize": 20
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                videos = data.get("data", {}).get("result", [])
                return self._process_videos(videos, days)
            else:
                logger.warning(f"API返回错误: {data.get('message')}")
                return []
                
        except Exception as e:
            logger.error(f"请求失败: {str(e)}")
            return []
    
    def _process_videos(self, videos: List[Dict], days: int) -> List[Dict[str, Any]]:
        """处理视频数据
        
        Args:
            videos: 原始视频数据
            days: 时间过滤
            
        Returns:
            处理后的视频列表
        """
        cutoff_time = datetime.now() - timedelta(days=days)
        processed = []
        
        for video in videos:
            pub_time = datetime.fromtimestamp(video.get("pubdate", 0))
            
            if pub_time < cutoff_time:
                continue
            
            processed.append({
                "bvid": video.get("bvid", ""),
                "title": video.get("title", ""),
                "author": video.get("author", ""),
                "description": video.get("description", ""),
                "duration": video.get("duration", 0),
                "pubdate": video.get("pubdate", 0),
                "play": video.get("play", 0),
                "like": video.get("like", 0),
                "comment": video.get("review", 0),
                "danmaku": video.get("video_review", 0),
                "pic": video.get("pic", "")
            })
        
        return processed
    
    def _deduplicate_videos(self, videos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """去重视频
        
        Args:
            videos: 视频列表
            
        Returns:
            去重后的视频列表
        """
        seen = set()
        unique = []
        
        for video in videos:
            bvid = video.get("bvid")
            if bvid and bvid not in seen:
                seen.add(bvid)
                unique.append(video)
        
        return unique
    
    def _rank_videos(self, videos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """视频排序打分
        
        Args:
            videos: 视频列表
            
        Returns:
            排序后的视频列表
        """
        for video in videos:
            score = self._calculate_score(video)
            video["hotspot_score"] = score
        
        return sorted(videos, key=lambda x: x["hotspot_score"], reverse=True)
    
    def _calculate_score(self, video: Dict[str, Any]) -> float:
        """计算视频热度分数
        
        Args:
            video: 视频数据
            
        Returns:
            热度分数
        """
        play = video.get("play", 0)
        like = video.get("like", 0)
        comment = video.get("comment", 0)
        danmaku = video.get("danmaku", 0)
        
        # 时间衰减
        pub_time = datetime.fromtimestamp(video.get("pubdate", 0))
        hours_old = (datetime.now() - pub_time).total_seconds() / 3600
        gravity = 1.8
        
        # 综合评分
        score = (
            play * 0.1 +
            like * 1.0 +
            comment * 0.8 +
            danmaku * 0.5
        ) / pow(hours_old + 2, gravity)
        
        return score

