#!/usr/bin/env bash

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATES="$REPO_ROOT/templates"
WORKSPACE="$HOME/opendaq-notebooks"

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    ACTIVATE="$REPO_ROOT/.venv/Scripts/activate"
else
    ACTIVATE="$REPO_ROOT/.venv/bin/activate"
fi

echo "Activating virtual environment."
source "$ACTIVATE"

mkdir -p "$WORKSPACE"
[ -f "$WORKSPACE/python_starter.ipynb" ] || cp "$TEMPLATES/python_template.ipynb" "$WORKSPACE/python_starter.ipynb"
[ -f "$WORKSPACE/csharp_starter.ipynb" ] || cp "$TEMPLATES/csharp_template.ipynb" "$WORKSPACE/csharp_starter.ipynb"

cd "$WORKSPACE"

echo "Starting JupyterLab."
jupyter lab --config="$REPO_ROOT/jupyter_config.py" python_starter.ipynb csharp_starter.ipynb
