"""应用测试"""

import pytest
from src.ui.app import create_app


@pytest.fixture
def app():
    """创建测试应用"""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()


def test_health(client):
    """测试健康检查端点"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'


def test_index(client):
    """测试首页"""
    response = client.get('/')
    assert response.status_code == 200


def test_create_task(client):
    """测试创建任务"""
    response = client.post('/api/tasks', data={
        'task_type': 'hotspot',
        'keywords': 'AI,测试',
        'user_input': '测试任务'
    })
    assert response.status_code == 200


def test_get_stats(client):
    """测试获取统计"""
    response = client.get('/api/stats')
    assert response.status_code == 200

