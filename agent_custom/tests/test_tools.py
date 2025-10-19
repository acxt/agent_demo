"""工具类测试"""

import pytest
from src.tools.hotspot import HotspotFinder


def test_hotspot_finder():
    """测试热点发现器"""
    finder = HotspotFinder()
    
    # 测试搜索（可能需要mock）
    # results = finder.find_hotspots(['AI'], top_k=5)
    # assert len(results) <= 5
    
    # 测试评分计算
    video = {
        'play': 10000,
        'like': 1000,
        'comment': 100,
        'danmaku': 50,
        'pubdate': 1700000000
    }
    score = finder._calculate_score(video)
    assert score > 0


def test_video_analyzer():
    """测试视频分析器"""
    from src.tools.analyzer import VideoAnalyzer
    
    analyzer = VideoAnalyzer()
    
    # 测试关键词提取
    comments = [
        {'content': 'AI 人工智能 很有趣'},
        {'content': '学习 AI 技术'},
    ]
    keywords = analyzer._extract_keywords(comments)
    assert 'AI' in keywords


def test_prompt_generator():
    """测试提示词生成器"""
    # 需要配置API密钥才能测试
    pass

