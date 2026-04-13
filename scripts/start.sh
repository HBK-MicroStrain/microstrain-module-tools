#!/usr/bin/env bash

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
