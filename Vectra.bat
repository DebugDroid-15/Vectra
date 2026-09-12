@echo off
setlocal enabledelayedexpansion
title Vectra - Scientific Computing Desktop Environment

echo =========================================================================
echo                   Vectra Desktop Scientific Computing
echo =========================================================================
echo Launching Vectra... Please wait.
echo.

:: 1. Activate virtual environment if present in root
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    set "PYTHON_EXE=python"
    goto :PYTHON_FOUND
)

:: 2. Test py launcher
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_EXE=py"
    goto :PYTHON_FOUND
)

:: 3. Test python executable (verifying it is NOT the Microsoft Store stub)
python -c "import sys; print(sys.version)" >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_EXE=python"
    goto :PYTHON_FOUND
)

:: 4. Search common Windows installation paths
if exist "%LocalAppData%\Programs\Python\Python311\python.exe" (
    set "PYTHON_EXE=%LocalAppData%\Programs\Python\Python311\python.exe"
    goto :PYTHON_FOUND
)
if exist "%LocalAppData%\Programs\Python\Python312\python.exe" (
    set "PYTHON_EXE=%LocalAppData%\Programs\Python\Python312\python.exe"
    goto :PYTHON_FOUND
)
if exist "%LocalAppData%\Programs\Python\Python310\python.exe" (
    set "PYTHON_EXE=%LocalAppData%\Programs\Python\Python310\python.exe"
    goto :PYTHON_FOUND
)
if exist "C:\Python311\python.exe" (
    set "PYTHON_EXE=C:\Python311\python.exe"
    goto :PYTHON_FOUND
)
if exist "C:\Python312\python.exe" (
    set "PYTHON_EXE=C:\Python312\python.exe"
    goto :PYTHON_FOUND
)

:PYTHON_NOT_FOUND
echo =========================================================================
echo [ERROR] Real Python executable was not found on your system!
echo =========================================================================
echo Windows redirected to the Microsoft Store stub ("Python was not found").
echo.
echo TO FIX THIS:
echo 1. Download & Install Python 3.10+ from: https://www.python.org/downloads/
echo 2. IMPORTANT: Check "Add python.exe to PATH" during installation!
echo 3. Disable Microsoft Store Aliases in:
echo    Start -> Settings -> Apps -> Advanced app settings -> App execution aliases
echo    (Turn OFF "App Installer: python.exe" and "python3.exe")
echo =========================================================================
echo.
pause
exit /b 9009

:PYTHON_FOUND
:: Install/Verify dependencies silently
echo [1/2] Verifying dependencies...
"%PYTHON_EXE%" -m pip install -q --disable-pip-version-check -e .
if %errorlevel% neq 0 (
    echo [WARNING] Automatic dependency check reported non-zero status. Attempting launch...
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
