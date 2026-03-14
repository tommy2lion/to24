#!/bin/bash
# 一键打包 to24 示例应用为独立可执行文件（自动处理虚拟环境和包安装）

set -e  # 遇到错误立即退出

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# 进入 python 目录（脚本的上层）
cd "$SCRIPT_DIR/.."

# 如果虚拟环境未激活，则尝试激活
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -f "./activate.sh" ]; then
        echo "🔄 Activating virtual environment..."
        source ./activate.sh
    else
        echo "❌ Virtual environment not active and activate.sh not found."
        exit 1
    fi
fi

# 进入 to24 项目目录
cd to24

echo "🧹 Uninstalling any editable to24 installation..."
# 忽略卸载错误（如果包不存在）
pip uninstall to24 -y 2>/dev/null || true

echo "📦 Installing to24 normally (non-editable)..."
pip install .

echo "🧹 Cleaning previous PyInstaller builds..."
rm -rf build dist app.spec

echo "🔨 Building executable with PyInstaller..."
pyinstaller --onefile --hidden-import to24 examples/app.py

echo "✅ Build complete! Executable is at: dist/app.exe"