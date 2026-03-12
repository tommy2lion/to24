#!/bin/bash
# Auto-enter to24 package directory and run pip install -e ., then return to original directory

set -e

# Save original directory
ORIG_DIR=$(pwd)

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Target directory: script_dir/../to24/to24
TARGET_DIR="$SCRIPT_DIR/../to24"

# Check if target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ Error: Target directory $TARGET_DIR not found."
    exit 1
fi

# Check if virtual environment is active (optional)
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: Virtual environment does not appear to be active. It's recommended to run 'source ../activate.sh' first."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "📦 Entering directory: $TARGET_DIR"
cd "$TARGET_DIR"

echo "🚀 Running pip install -e ."
pip install -e .

echo "✅ Installation complete. Returning to: $ORIG_DIR"
cd "$ORIG_DIR"