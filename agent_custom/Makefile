# VideoAgent Makefile

.PHONY: help install run test clean check dev

help:
	@echo "VideoAgent - 可用命令："
	@echo "  make install  - 安装依赖"
	@echo "  make run      - 启动应用"
	@echo "  make dev      - 开发模式启动"
	@echo "  make test     - 运行测试"
	@echo "  make check    - 环境检查"
	@echo "  make clean    - 清理缓存"

install:
	pip install -r requirements.txt

run:
	python main.py

dev:
	FLASK_ENV=development python main.py

test:
	pytest tests/ -v

check:
	python scripts/check_env.py

clean:
	python scripts/clean.py
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

