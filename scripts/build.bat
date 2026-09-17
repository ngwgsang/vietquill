@echo off

call scripts\clean.bat

set "PYTHON=python"

if exist "venv\Scripts\python.exe" (
    set "PYTHON=venv\Scripts\python.exe"
)

%PYTHON% -m build
if errorlevel 1 exit /b %errorlevel%

%PYTHON% -m twine check dist\*