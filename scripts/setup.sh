#!/usr/bin/env bash

# Change to the project root so all relative paths work regardless of where this
# script was called from.
cd "$(dirname "${BASH_SOURCE[0]}")/.."

INSTALL_CSHARP=false

for arg in "$@"; do
    case $arg in
        --csharp) INSTALL_CSHARP=true ;;
        *)
            echo "Unknown option: $arg"
            echo "Usage: setup.sh [--csharp]"
            exit 1
            ;;
    esac
done

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    PYTHON="python"
    ACTIVATE=".venv/Scripts/activate"
    DOTNET_JUPYTER_DIR="$(cygpath -u "$USERPROFILE")/.dotnet-jupyter"
    DOTNET_JUPYTER_WIN="$USERPROFILE\\.dotnet-jupyter"
else
    PYTHON="python3"
    ACTIVATE=".venv/bin/activate"
    DOTNET_JUPYTER_DIR="$HOME/.dotnet-jupyter"
fi

if [[ -d ".venv" ]]; then
    echo "Removing existing virtual environment."
    rm -rf .venv
fi

echo "Setting up virtual environment."
$PYTHON -m venv .venv

echo "Activating virtual environment."
source "$ACTIVATE"

echo "Installing Python dependencies."
pip install -r requirements.txt

if [[ "$INSTALL_CSHARP" == true ]]; then
    if [[ ! -d "$DOTNET_JUPYTER_DIR" ]]; then
        echo "Setting up dedicated .NET environment for Jupyter."
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
            powershell -ExecutionPolicy Bypass -Command "& ([scriptblock]::Create((Invoke-RestMethod https://dot.net/v1/dotnet-install.ps1))) -Channel 8.0 -InstallDir \"$DOTNET_JUPYTER_WIN\""
        else
            curl -sSL https://dot.net/v1/dotnet-install.sh | bash /dev/stdin --channel 8.0 --install-dir "$DOTNET_JUPYTER_DIR"
        fi

        echo "Installing C# Jupyter kernel."
        "$DOTNET_JUPYTER_DIR/dotnet" tool install Microsoft.dotnet-interactive --tool-path "$DOTNET_JUPYTER_DIR/tools"
        "$DOTNET_JUPYTER_DIR/tools/dotnet-interactive" jupyter install
    else
        echo "Dedicated .NET environment for Jupyter already exists, skipping."
    fi
fi

echo "Setup complete. Run scripts/start.sh to begin a session."
