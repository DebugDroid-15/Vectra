@echo off
setlocal enabledelayedexpansion
title Vectra - Scientific Computing Desktop Environment

echo =========================================================================
echo                   Vectra Desktop Scientific Computing
echo =========================================================================
echo Launching Vectra... Please wait.
echo.

:: Detect Python binary executable
set PYTHON_EXE=
where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PYTHON_EXE=python"
) else (
    where py >nul 2>nul
    if %errorlevel% equ 0 (
        set "PYTHON_EXE=py"
    )
)

if "%PYTHON_EXE%"=="" (
    echo [ERROR] Python is not installed or not added to system PATH.
    echo Please install Python 3.10+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 9009
)

:: Activate virtual environment if present in root
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    set "PYTHON_EXE=python"
)

:: Install/Verify dependencies silently
echo [1/2] Verifying dependencies...
"%PYTHON_EXE%" -m pip install -q --disable-pip-version-check -e .
if %errorlevel% neq 0 (
    echo [WARNING] Automatic dependency check reported non-zero status. Proceeding to launch...
)

:: Launch Vectra Desktop IDE
echo [2/2] Starting Vectra Desktop IDE...
echo =========================================================================
echo.

"%PYTHON_EXE%" -m kheramat.gui.app

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Vectra exited with code: %errorlevel%
    echo Check log records in: %USERPROFILE%\.vectra\logs\vectra_app.log
    pause
)

