"""应用入口"""

from src.ui.app import create_app
from src.core.config import get_settings
from src.core.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


def main():
    """启动应用"""
    logger.info("=" * 60)
    logger.info("VideoAgent - AI视频创作助手")
    logger.info("=" * 60)
    logger.info(f"服务地址: http://{settings.api_host}:{settings.api_port}")
    logger.info(f"调试模式: {settings.debug}")
    logger.info("=" * 60)
    
    # 创建并运行Flask应用
    app = create_app()
    app.run(
        host=settings.api_host,
        port=settings.api_port,
        debug=settings.debug
    )


if __name__ == "__main__":
    main()

