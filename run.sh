#!/bin/bash

# Get the directory where this script is located
THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

function test() {
    pytest \
    --cov="$THIS_DIR"/src/create_python_project \
    --cov-report=html \
    --cov-config=pyproject.toml \
    --cov-fail-under=99 \
    "$@"
}

function clean() {
    echo "Cleaning Python build distribution artifacts..."

    # Remove Python byte code files and __pycache__ directories
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete
    find . -type f -name "*.pyd" -delete

    # Remove build directories
    rm -rf build/
    rm -rf dist/
    rm -rf .eggs/
    rm -rf ./**/*.egg-info/

    # Remove test and coverage artifacts
    rm -rf .pytest_cache/
    rm -rf .coverage
    rm -rf htmlcov/
    rm -rf .tox/

    echo "Clean completed!"
}

function build() {
    python -m build
}

# Get the function name from the first argument
function_name=$1
shift

# Call the function with the remaining arguments
if [ -n "$function_name" ] && type "$function_name" | grep -q "function" 2>/dev/null; then
    "$function_name" "$@"
else
    echo "Error: Function '$function_name' not found."
    echo "Available functions:"
    declare -F | cut -d' ' -f3
    exit 1
fi
