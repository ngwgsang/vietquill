@echo off

call scripts\build.bat
if errorlevel 1 exit /b %errorlevel%

set "PYTHON=python"
if exist "venv\Scripts\python.exe" (
    set "PYTHON=venv\Scripts\python.exe"
)

%PYTHON% -m twine upload dist\*