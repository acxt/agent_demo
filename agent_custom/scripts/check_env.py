"""环境检查脚本"""

import os
from pathlib import Path


def check_environment():
    """检查环境配置"""
    print("=" * 60)
    print("环境检查")
    print("=" * 60)
    
    errors = []
    warnings = []
    
    # 检查.env文件
    if not Path(".env").exists():
        errors.append("❌ .env文件不存在")
    else:
        print("✓ .env文件存在")
    
    # 检查必需的环境变量
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = {
        "GEMINI_API_KEYS": "Gemini API密钥",
        "BILI_COOKIE": "B站Cookie"
    }
    
    for var, desc in required_vars.items():
        if not os.getenv(var):
            errors.append(f"❌ 缺少必需配置: {var} ({desc})")
        else:
            print(f"✓ {desc}已配置")
    
    # 检查可选配置
    optional_vars = {
        "VEO_API_KEY": "VEO API密钥",
        "DEEPSEEK_API_KEY": "DeepSeek API密钥"
    }
    
    for var, desc in optional_vars.items():
        if not os.getenv(var):
            warnings.append(f"⚠ 未配置: {var} ({desc})")
        else:
            print(f"✓ {desc}已配置")
    
    # 检查目录
    required_dirs = ["data", "logs", "config"]
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            warnings.append(f"⚠ 目录不存在: {dir_name}")
        else:
            print(f"✓ {dir_name}目录存在")
    
    # 输出结果
    print("\n" + "=" * 60)
    
    if warnings:
        print("\n警告:")
        for warning in warnings:
            print(warning)
    
    if errors:
        print("\n错误:")
        for error in errors:
            print(error)
        print("\n请修复以上错误后再启动应用")
        return False
    else:
        print("\n✓ 环境检查通过")
        return True


if __name__ == "__main__":
    success = check_environment()
    exit(0 if success else 1)

