#!/usr/bin/env bash

# Change to the project root so all relative paths work regardless of where this
# script was called from.
cd "$(dirname "${BASH_SOURCE[0]}")/.."

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    PYTHON="python"
    ACTIVATE=".venv/Scripts/activate"
else
    PYTHON="python3"
    ACTIVATE=".venv/bin/activate"
fi

if [[ -d ".venv" ]]; then
    echo "Removing existing virtual environment."
    rm -rf .venv
fi

echo "Setting up virtual environment."
$PYTHON -m venv .venv

echo "Activating virtual environment."
source "$ACTIVATE"

echo "Installing dependencies."
pip install -r requirements.txt

echo "Setup complete. Run scripts/start.sh to begin a session."
