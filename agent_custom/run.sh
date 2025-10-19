#!/bin/bash

echo "VideoAgent - AI视频创作助手"
echo "====================================="

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "未找到虚拟环境，正在创建..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "检查依赖..."
pip install -r requirements.txt --quiet

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "警告: 未找到.env文件，请复制env_example.txt为.env并配置"
fi

# 启动应用
echo "启动应用..."
echo "====================================="
python main.py

