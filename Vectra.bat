@echo off
setlocal enabledelayedexpansion
title Vectra - Scientific Computing Desktop Environment

echo =========================================================================
echo                   Vectra Desktop Scientific Computing
echo =========================================================================
echo Launching Vectra... Please wait.
echo.

:: Check Python installation
where python >nul 2>nul
if %errorlevel% neq 0 (
    where py >nul 2>nul
    if %errorlevel% neq 0 (
        echo [ERROR] Python 3 is not installed or not added to PATH.
        echo Please install Python 3.10 or higher from https://www.python.org/
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
    )
) else (
    set PYTHON_CMD=python
)

:: Install/Verify dependencies silently
echo [1/2] Verifying dependencies...
%PYTHON_CMD% -m pip install -q --disable-pip-version-check -e .

:: Launch Vectra Desktop IDE
echo [2/2] Starting Vectra Desktop IDE...
echo =========================================================================
echo.

%PYTHON_CMD% -m kheramat.gui.app

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Vectra closed with an error code: %errorlevel%
    pause
)

