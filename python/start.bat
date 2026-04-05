@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

rem переходим из python\ в OPENMODEL\
cd /d "%~dp0.."

rem путь к python.exe (он в текущей папке python\)
set "PYTHON_EXE=%~dp0python.exe"

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Python not found at: "%PYTHON_EXE%"
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