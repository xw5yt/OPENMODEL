@echo off
chcp 65001 >nul
setlocal

cd /d "%~dp0.."

set "PYTHON_EXE=%cd%\python\python.exe"

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Python not found: "%PYTHON_EXE%"
    pause
    exit /b 1
)

if exist "requirements.txt" (
    "%PYTHON_EXE%" -m pip install -q --upgrade pip
    "%PYTHON_EXE%" -m pip install -q -r requirements.txt
)

"%PYTHON_EXE%" main.py

if errorlevel 1 (
    echo.
    echo [ERROR] main.py crashed
)

pause