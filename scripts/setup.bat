@echo off

echo Setting up virtual environment.
python -m venv .venv

echo Activating virtual environment.
call .venv\Scripts\activate

echo Installing dependencies.
pip install -r requirements.txt

echo Setup complete. Run scripts/start.bat to begin a session.