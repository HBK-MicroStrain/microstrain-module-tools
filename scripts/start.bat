@echo off

rem Change to the project root so all relative paths work regardless of where this
rem script was called from.
cd /d "%~dp0.."

echo Activating virtual environment.
call .venv\Scripts\activate

echo Starting JupyterLab.
jupyter lab