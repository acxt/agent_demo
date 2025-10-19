# VideoAgent 启动脚本

Write-Host "VideoAgent - AI视频创作助手" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# 检查虚拟环境
if (-not (Test-Path "venv")) {
    Write-Host "未找到虚拟环境，正在创建..." -ForegroundColor Yellow
    python -m venv venv
}

# 激活虚拟环境
Write-Host "激活虚拟环境..." -ForegroundColor Green
& "venv\Scripts\Activate.ps1"

# 安装依赖
Write-Host "检查依赖..." -ForegroundColor Green
pip install -r requirements.txt --quiet

# 检查.env文件
if (-not (Test-Path ".env")) {
    Write-Host "警告: 未找到.env文件，请复制env_example.txt为.env并配置" -ForegroundColor Yellow
}

# 启动应用
Write-Host "启动应用..." -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
python main.py

