#!/usr/bin/env bash

# Change to the project root so all relative paths work regardless of where this
# script was called from.
cd "$(dirname "${BASH_SOURCE[0]}")/.."

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    ACTIVATE=".venv/Scripts/activate"
    PYTHON="python"
else
    ACTIVATE=".venv/bin/activate"
    PYTHON="python3"
fi

echo "Activating virtual environment."
source "$ACTIVATE"

echo "Starting interactive session."
$PYTHON -i daq_setup.py
