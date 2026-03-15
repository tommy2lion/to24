#!/bin/bash
# One-click build to24 example app as a standalone executable (auto-handles virtual env and package installation)

set -e  # Exit immediately on error

# Get absolute path of the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Enter the python directory (one level above the script)
cd "$SCRIPT_DIR/.."

# If virtual environment is not active, try to activate it
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -f "./activate.sh" ]; then
        echo "🔄 Activating virtual environment..."
        source ./activate.sh
    else
        echo "❌ Virtual environment not active and activate.sh not found."
        exit 1
    fi
fi

# Enter the to24 project directory
cd to24

echo "🧹 Uninstalling any editable to24 installation..."
# Ignore uninstall errors (in case the package is not installed)
pip uninstall to24 -y 2>/dev/null || true

echo "📦 Installing to24 normally (non-editable)..."
pip install .

echo "🧹 Cleaning previous PyInstaller builds..."
rm -rf build dist app.spec

echo "🔨 Building executable with PyInstaller..."
pyinstaller --onefile --hidden-import to24 examples/app.py

echo "✅ Build complete! Executable is at: dist/app.exe"