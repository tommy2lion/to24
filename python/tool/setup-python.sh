#!/bin/bash
# ============================================================
# 智能 Python 学习环境配置脚本（自动检测 Python 版本）
# 用法：
#   ./setup-python.sh
#   该脚本必须位于项目 python/tool/ 目录下。
#   它会在上级目录（python/）中创建虚拟环境、activate.sh 和 VSCode 配置。
# ============================================================

set -e

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# 项目根目录（python/）是脚本所在目录的上一级
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "📁 项目根目录: $PROJECT_ROOT"

# ---------- 可选：手动指定 Python 路径（取消注释并填写）----------
# PYTHON_PATH="/c/Python314/python.exe"
# -------------------------------------------------------------

echo "🚀 开始配置 Python 学习环境..."

# ----- 1. 检测 Python 位置和版本 -----
if [ -z "$PYTHON_PATH" ]; then
    if command -v python &> /dev/null; then
        PYTHON_PATH=$(which python)
    else
        echo "❌ 未找到 Python，请安装或手动指定 PYTHON_PATH"
        exit 1
    fi
fi
echo "🔍 Python: $PYTHON_PATH"

PY_VERSION=$("$PYTHON_PATH" --version 2>&1 | awk '{print $2}' | awk -F. '{print $1$2}')
if [ -z "$PY_VERSION" ]; then
    echo "❌ 无法获取 Python 版本"
    exit 1
fi
echo "📌 版本: $PY_VERSION"

# ----- 2. 设置虚拟环境 -----
VENV_NAME="venv$PY_VERSION"
VENV_PATH="$PROJECT_ROOT/$VENV_NAME"
echo "📁 虚拟环境: $VENV_PATH"

# ----- 3. 进入项目根目录 -----
cd "$PROJECT_ROOT"

# ----- 4. 创建虚拟环境 -----
"$PYTHON_PATH" -m venv "$VENV_NAME"
echo "✅ 虚拟环境 $VENV_NAME 创建成功"

# ----- 5. 生成激活脚本 activate.sh -----
if [ -f "$VENV_PATH/Scripts/activate" ]; then
    ACTIVATE_SCRIPT="./${VENV_NAME}/Scripts/activate"
elif [ -f "$VENV_PATH/bin/activate" ]; then
    ACTIVATE_SCRIPT="./${VENV_NAME}/bin/activate"
else
    echo "⚠️ 无法找到激活脚本，请手动激活"
    ACTIVATE_SCRIPT=""
fi

if [ -n "$ACTIVATE_SCRIPT" ]; then
    cat > "$PROJECT_ROOT/activate.sh" << EOF
#!/bin/bash
if [[ "\${BASH_SOURCE[0]}" == "\${0}" ]]; then
    echo "❌ 请使用 source activate.sh"
    exit 1
fi
source "$ACTIVATE_SCRIPT"
EOF
    chmod +x "$PROJECT_ROOT/activate.sh"
    echo "✅ 已生成 activate.sh"
else
    echo "⚠️ 跳过生成 activate.sh"
fi

# ----- 6. 安装 VSCode Python 扩展 -----
if command -v code &> /dev/null; then
    code --install-extension ms-python.python --force
    echo "✅ VSCode Python 扩展安装完成"
else
    echo "⚠️ 未找到 code 命令，请手动安装扩展"
fi

# ----- 7. 配置 VSCode 工作区（使用绝对路径）-----
mkdir -p "$PROJECT_ROOT/.vscode"
if [ -d "$VENV_PATH/Scripts" ]; then
    PYTHON_INTERPRETER="$VENV_PATH/Scripts/python.exe"
else
    PYTHON_INTERPRETER="$VENV_PATH/bin/python"
fi

cat > "$PROJECT_ROOT/.vscode/settings.json" << EOF
{
    "python.defaultInterpreterPath": "$PYTHON_INTERPRETER",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true
}
EOF
echo "✅ VSCode 工作区配置完成"

# ----- 8. 完成提示 -----
echo ""
echo "🎉 全部完成！"
echo "👉 项目位置: $PROJECT_ROOT"
echo "👉 虚拟环境: $VENV_NAME (已创建，未激活)"
echo "👉 激活命令: cd $PROJECT_ROOT && source activate.sh"
echo "👉 VSCode 设置已配置（使用绝对路径）"
echo ""