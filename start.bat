@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

cd /d "%~dp0"

set "PYTHON_EXE=%~dp0python\python.exe"

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Python не найден по пути: "%PYTHON_EXE%"
    echo Убедитесь, что папка 'python' находится рядом с этим файлом.
    pause
    exit /b 1
)

echo [INFO] Используется Python: "%PYTHON_EXE%"

if not exist "requirements.txt" (
    echo [WARN] requirements.txt не найден. Пропускаю установку зависимостей.
    goto :run_main
)

echo [INFO] Проверка и установка зависимостей...
echo.

"%PYTHON_EXE%" -m pip install --upgrade pip
"%PYTHON_EXE%" -m pip install requests

echo [INFO] Установка пакетов из requirements.txt...
"%PYTHON_EXE%" -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [WARN] Некоторые пакеты не удалось установить. Попробуем запустить проект...
    echo.
) else (
    echo [SUCCESS] Все зависимости установлены.
    echo.
)

:run_main
echo [START] Запуск OPENMODEL AI...
echo.

"%PYTHON_EXE%" main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Произошла ошибка при выполнении main.py
    pause
)

pause