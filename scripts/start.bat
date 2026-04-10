@echo off

echo Activating virtual environment.
call .venv\Scripts\activate

echo Starting interactive session.
python -i daq_setup.py