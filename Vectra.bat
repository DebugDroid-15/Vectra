@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
title Vectra - Scientific Computing Desktop Environment

echo =========================================================================
echo                   VECTRA DESKTOP SCIENTIFIC COMPUTING
echo =========================================================================
echo Initializing Vectra Desktop Platform...
echo.

set "SYS_PYTHON="

:: 1. Auto-Scan & Locate Python Environment
echo [1/4] Scanning system and local directory for Python installation...

if exist ".venv\Scripts\python.exe" (
    set "SYS_PYTHON=.venv\Scripts\python.exe"
    echo [INFO] Found local virtual environment at .venv
    goto :RUN_SETUP
)

py -c "import sys; print(sys.version)" >nul 2>&1
if !errorlevel! equ 0 (
    set "SYS_PYTHON=py"
    echo [INFO] Detected Python via Windows 'py' launcher
    goto :RUN_SETUP
)

python -c "import sys; print(sys.version)" >nul 2>&1
if !errorlevel! equ 0 (
    set "SYS_PYTHON=python"
    echo [INFO] Detected Python from system PATH
    goto :RUN_SETUP
)

python3 -c "import sys; print(sys.version)" >nul 2>&1
if !errorlevel! equ 0 (
    set "SYS_PYTHON=python3"
    echo [INFO] Detected python3 from system PATH
    goto :RUN_SETUP
)

:: Scan standard installation paths
for /d %%D in ("%LocalAppData%\Programs\Python\Python*") do (
    if exist "%%D\python.exe" (
        "%%D\python.exe" -c "import sys; print(sys.version)" >nul 2>&1
        if !errorlevel! equ 0 (
            set "SYS_PYTHON=%%D\python.exe"
            echo [INFO] Detected Python at %%D\python.exe
            goto :RUN_SETUP
        )
    )
)

for /d %%D in ("C:\Python*") do (
    if exist "%%D\python.exe" (
        "%%D\python.exe" -c "import sys; print(sys.version)" >nul 2>&1
        if !errorlevel! equ 0 (
            set "SYS_PYTHON=%%D\python.exe"
            echo [INFO] Detected Python at %%D\python.exe
            goto :RUN_SETUP
        )
    )
)

for /d %%D in ("C:\Program Files\Python*") do (
    if exist "%%D\python.exe" (
        "%%D\python.exe" -c "import sys; print(sys.version)" >nul 2>&1
        if !errorlevel! equ 0 (
            set "SYS_PYTHON=%%D\python.exe"
            echo [INFO] Detected Python at %%D\python.exe
            goto :RUN_SETUP
        )
    )
)

for /d %%D in ("%ProgramData%\Anaconda3*" "%ProgramData%\Miniconda3*" "%UserProfile%\Anaconda3*" "%UserProfile%\Miniconda3*") do (
    if exist "%%D\python.exe" (
        "%%D\python.exe" -c "import sys; print(sys.version)" >nul 2>&1
        if !errorlevel! equ 0 (
            set "SYS_PYTHON=%%D\python.exe"
            echo [INFO] Detected Conda Python at %%D\python.exe
            goto :RUN_SETUP
        )
    )
)

:NOT_FOUND
echo.
echo =========================================================================
echo [ERROR] No compatible Python installation was found on this machine!
echo =========================================================================
echo Vectra requires Python 3.10 or newer to run.
echo.
echo Quick Resolution Steps:
echo   1. Download Python: https://www.python.org/downloads/
echo   2. Run installer and CHECK "Add python.exe to PATH"
echo   3. Re-run Vectra.bat
echo =========================================================================
echo.
pause
exit /b 9009

:RUN_SETUP
echo.
echo [2/4] Executing Vectra Automated Setup Wizard with Live Progress...
echo.

"%SYS_PYTHON%" src\kheramat\setup_wizard.py

set "PYTHON_EXE=.venv\Scripts\python.exe"
if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=%SYS_PYTHON%"
)

echo [3/4] Validating runtime binaries and graphical dependencies...
"%PYTHON_EXE%" -c "import PySide6, numpy, matplotlib" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing required GUI libraries (PySide6)...
    "%PYTHON_EXE%" -m pip install PySide6 numpy matplotlib
)

echo [4/4] Launching Vectra Graphical Desktop Environment...
echo =========================================================================
echo.

"%PYTHON_EXE%" -m kheramat.gui.app

if %errorlevel% neq 0 (
    echo.
    echo =========================================================================
    echo [CRITICAL ERROR] Vectra Desktop application crashed or exited with error code: %errorlevel%
    echo =========================================================================
    echo Log file saved at: %USERPROFILE%\.vectra\logs\vectra_app.log
    echo.
    pause
)

