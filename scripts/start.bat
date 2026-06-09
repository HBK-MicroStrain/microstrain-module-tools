@echo off

set REPO_ROOT=%~dp0..
set TEMPLATES=%~dp0..\templates
set WORKSPACE=%USERPROFILE%\opendaq-notebooks

echo Activating virtual environment.
call "%REPO_ROOT%\.venv\Scripts\activate"

if not exist "%WORKSPACE%" mkdir "%WORKSPACE%"
if not exist "%WORKSPACE%\python_starter.ipynb" copy "%TEMPLATES%\python_template.ipynb" "%WORKSPACE%\python_starter.ipynb" > nul
if not exist "%WORKSPACE%\csharp_starter.ipynb" copy "%TEMPLATES%\csharp_template.ipynb" "%WORKSPACE%\csharp_starter.ipynb" > nul

cd /d "%WORKSPACE%"

echo Starting JupyterLab.
jupyter lab --config="%REPO_ROOT%\jupyter_config.py" python_starter.ipynb csharp_starter.ipynb