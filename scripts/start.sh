#!/usr/bin/env bash

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKSPACE="$HOME/opendaq-notebooks"

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    ACTIVATE="$REPO_ROOT/.venv/Scripts/activate"
else
    ACTIVATE="$REPO_ROOT/.venv/bin/activate"
fi

if [[ ! -d "$WORKSPACE" ]]; then
    echo "Workspace not found. Run scripts/setup.sh --python and/or --csharp first."
    exit 1
fi

echo "Activating virtual environment."
source "$ACTIVATE"

cd "$WORKSPACE"

OPEN_FILES=()
[[ -f "python_starter.ipynb" ]] && OPEN_FILES+=("python_starter.ipynb")
[[ -f "csharp_starter.ipynb" ]] && OPEN_FILES+=("csharp_starter.ipynb")

if [[ ${#OPEN_FILES[@]} -eq 0 ]]; then
    echo "No starter notebooks found. Run scripts/setup.sh --python and/or --csharp first."
    exit 1
fi

echo "Starting JupyterLab."
jupyter lab --config="$REPO_ROOT/jupyter_config.py" "${OPEN_FILES[@]}"
