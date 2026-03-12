#!/bin/bash
# ============================================================
# Smart Python Learning Environment Setup Script
# Usage:
#   ./setup-python-en.sh
#   This script must be placed in the project's python/tool/ directory.
#   It will create virtual environment, activate.sh, and VSCode config in the parent directory (python/).
# ============================================================

set -e

# Get absolute path of script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Project root (python/) is one level above script directory
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "📁 Project root: $PROJECT_ROOT"

# ---------- Optional: manually set Python path ----------
# PYTHON_PATH="/c/Python314/python.exe"
# -------------------------------------------------------------

echo "🚀 Starting Python environment setup..."

# ----- 1. Detect Python location and version -----
if [ -z "$PYTHON_PATH" ]; then
    if command -v python &> /dev/null; then
        PYTHON_PATH=$(which python)
    else
        echo "❌ Python not found. Please install or set PYTHON_PATH."
        exit 1
    fi
fi
echo "🔍 Python: $PYTHON_PATH"

PY_VERSION=$("$PYTHON_PATH" --version 2>&1 | awk '{print $2}' | awk -F. '{print $1$2}')
if [ -z "$PY_VERSION" ]; then
    echo "❌ Could not determine Python version."
    exit 1
fi
echo "📌 Version: $PY_VERSION"

# ----- 2. Set virtual environment -----
VENV_NAME="venv$PY_VERSION"
VENV_PATH="$PROJECT_ROOT/$VENV_NAME"
echo "📁 Virtual environment: $VENV_PATH"

# ----- 3. Enter project root -----
cd "$PROJECT_ROOT"

# ----- 4. Create virtual environment -----
"$PYTHON_PATH" -m venv "$VENV_NAME"
echo "✅ Virtual environment $VENV_NAME created."

# ----- 5. Generate activation helper script activate.sh -----
if [ -f "$VENV_PATH/Scripts/activate" ]; then
    ACTIVATE_SCRIPT="./${VENV_NAME}/Scripts/activate"
elif [ -f "$VENV_PATH/bin/activate" ]; then
    ACTIVATE_SCRIPT="./${VENV_NAME}/bin/activate"
else
    echo "⚠️ Cannot find activate script. Please activate manually."
    ACTIVATE_SCRIPT=""
fi

if [ -n "$ACTIVATE_SCRIPT" ]; then
    cat > "$PROJECT_ROOT/activate.sh" << EOF
#!/bin/bash
if [[ "\${BASH_SOURCE[0]}" == "\${0}" ]]; then
    echo "❌ Please use 'source activate.sh'"
    exit 1
fi
source "$ACTIVATE_SCRIPT"
EOF
    chmod +x "$PROJECT_ROOT/activate.sh"
    echo "✅ Generated activate.sh"
else
    echo "⚠️ Skipped activate.sh generation."
fi

# ----- 6. Install VSCode Python extension -----
if command -v code &> /dev/null; then
    code --install-extension ms-python.python --force
    echo "✅ VSCode Python extension installed."
else
    echo "⚠️ VSCode command not found. Please install extension manually."
fi

# ----- 7. Configure VSCode workspace (using absolute path) -----
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
echo "✅ VSCode workspace configured."

# ----- 8. Final instructions -----
echo ""
echo "🎉 All done!"
echo "👉 Project location: $PROJECT_ROOT"
echo "👉 Virtual env: $VENV_NAME (created, not activated)"
echo "👉 Activate it: cd $PROJECT_ROOT && source activate.sh"
echo "👉 VSCode settings configured (using absolute path)"
echo ""