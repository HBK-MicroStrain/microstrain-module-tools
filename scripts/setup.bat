@echo off

rem Change to the project root so all relative paths work regardless of where this
rem script was called from.
cd /d "%~dp0.."

if exist .venv (
    echo Removing existing virtual environment.
    rmdir /s /q .venv
)

echo Setting up virtual environment.
python -m venv .venv

echo Activating virtual environment.
call .venv\Scripts\activate

echo Installing dependencies.
pip install -r requirements.txt

echo Setup complete. Run scripts/start.bat to begin a session.