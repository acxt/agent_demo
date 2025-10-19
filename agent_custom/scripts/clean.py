"""清理脚本 - 删除临时文件和缓存"""

import shutil
from pathlib import Path


def clean():
    """清理项目"""
    print("开始清理项目...")
    
    # 要清理的目录和文件
    patterns = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
        ".pytest_cache",
        "**/.pytest_cache",
        "*.egg-info",
        "dist",
        "build",
        ".coverage",
        "htmlcov",
        "logs/*.log",
    ]
    
    cleaned = []
    
    for pattern in patterns:
        for path in Path(".").glob(pattern):
            try:
                if path.is_file():
                    path.unlink()
                    cleaned.append(str(path))
                    print(f"删除文件: {path}")
                elif path.is_dir():
                    shutil.rmtree(path)
                    cleaned.append(str(path))
                    print(f"删除目录: {path}")
            except Exception as e:
                print(f"无法删除 {path}: {e}")
    
    if cleaned:
        print(f"\n清理完成，共删除 {len(cleaned)} 项")
    else:
        print("\n没有需要清理的内容")


if __name__ == "__main__":
    clean()

