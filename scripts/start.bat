@echo off

set REPO_ROOT=%~dp0..
set WORKSPACE=%USERPROFILE%\opendaq-notebooks

if not exist "%WORKSPACE%" (
    echo Workspace not found. Run scripts\setup.bat --python and/or --csharp first.
    exit /b 1
)

echo Activating virtual environment.
call "%REPO_ROOT%\.venv\Scripts\activate"

cd /d "%WORKSPACE%"

set OPEN_FILES=
if exist "%WORKSPACE%\python_starter.ipynb" set OPEN_FILES=python_starter.ipynb
if exist "%WORKSPACE%\csharp_starter.ipynb" set OPEN_FILES=%OPEN_FILES% csharp_starter.ipynb

if "%OPEN_FILES%"=="" (
    echo No starter notebooks found. Run scripts\setup.bat --python and/or --csharp first.
    exit /b 1
)

echo Starting JupyterLab.
jupyter lab --config="%REPO_ROOT%\jupyter_config.py" %OPEN_FILES%