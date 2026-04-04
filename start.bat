@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

cd /d "%~dp0"

set "PYTHON_EXE=%~dp0python\python.exe"

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Python not found at: "%PYTHON_EXE%"
    echo Make sure the 'python' folder is next to this file.
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo [WARN] requirements.txt not found. Skipping dependency install.
    goto :run_main
)

"%PYTHON_EXE%" -m pip install -q --upgrade pip
"%PYTHON_EXE%" -m pip install -q -r requirements.txt

if errorlevel 1 (
    echo [WARN] Some packages failed to install. Trying to run anyway...
)

:run_main
"%PYTHON_EXE%" main.py

if errorlevel 1 (
    echo.
    echo [ERROR] main.py exited with an error.
    pause
)

pause