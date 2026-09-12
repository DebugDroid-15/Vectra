@echo off
setlocal enabledelayedexpansion
title Vectra - Scientific Computing Desktop Environment

echo =========================================================================
echo                   Vectra Desktop Scientific Computing
echo =========================================================================
echo Launching Vectra... Please wait.
echo.

set "SYS_PYTHON="

:: 1. Check local virtual environment (.venv)
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
    echo [INFO] Using existing virtual environment at .venv
    goto :RUN_VECTRA
)

:: 2. Try 'py' launcher
py -c "import sys; print(sys.version)" >nul 2>&1
if !errorlevel! equ 0 (
    set "SYS_PYTHON=py"
    echo [INFO] Detected Python via Windows 'py' launcher
    goto :CREATE_VENV
)

:: 3. Try system 'python' command (ensuring it's not the Windows Store 0-byte stub)
python -c "import sys; print(sys.version)" >nul 2>&1
if !errorlevel! equ 0 (
    set "SYS_PYTHON=python"
    echo [INFO] Detected Python from system PATH
    goto :CREATE_VENV
)

:: 4. Try system 'python3' command
python3 -c "import sys; print(sys.version)" >nul 2>&1
if !errorlevel! equ 0 (
    set "SYS_PYTHON=python3"
    echo [INFO] Detected python3 from system PATH
    goto :CREATE_VENV
)

:: 5. Auto-scan all standard Python & Conda installation directories
for /d %%D in ("%LocalAppData%\Programs\Python\Python*") do (
    if exist "%%D\python.exe" (
        "%%D\python.exe" -c "import sys; print(sys.version)" >nul 2>&1
        if !errorlevel! equ 0 (
            set "SYS_PYTHON=%%D\python.exe"
            echo [INFO] Detected Python at %%D\python.exe
            goto :CREATE_VENV
        )
    )
)

for /d %%D in ("C:\Python*") do (
    if exist "%%D\python.exe" (
        "%%D\python.exe" -c "import sys; print(sys.version)" >nul 2>&1
        if !errorlevel! equ 0 (
            set "SYS_PYTHON=%%D\python.exe"
            echo [INFO] Detected Python at %%D\python.exe
            goto :CREATE_VENV
        )
    )
)

for /d %%D in ("C:\Program Files\Python*") do (
    if exist "%%D\python.exe" (
        "%%D\python.exe" -c "import sys; print(sys.version)" >nul 2>&1
        if !errorlevel! equ 0 (
            set "SYS_PYTHON=%%D\python.exe"
            echo [INFO] Detected Python at %%D\python.exe
            goto :CREATE_VENV
        )
    )
)

for /d %%D in ("%ProgramData%\Anaconda3*" "%ProgramData%\Miniconda3*" "%UserProfile%\Anaconda3*" "%UserProfile%\Miniconda3*") do (
    if exist "%%D\python.exe" (
        "%%D\python.exe" -c "import sys; print(sys.version)" >nul 2>&1
        if !errorlevel! equ 0 (
            set "SYS_PYTHON=%%D\python.exe"
            echo [INFO] Detected Conda Python environment at %%D\python.exe
            goto :CREATE_VENV
        )
    )
)

:NOT_FOUND
echo =========================================================================
echo [ERROR] No working Python installation was found on this system!
echo =========================================================================
echo.
echo Please install Python 3.10+:
echo 1. Download Python from: https://www.python.org/downloads/
echo 2. Check the box "Add python.exe to PATH" during installation!
echo.
pause
exit /b 9009

:CREATE_VENV
echo [1/3] Creating isolated virtual environment (.venv)...
"%SYS_PYTHON%" -m venv .venv
if !errorlevel! neq 0 (
    echo [WARNING] Could not create virtual environment. Running with system Python...
    set "PYTHON_EXE=%SYS_PYTHON%"
    goto :INSTALL_DEPS
)
set "PYTHON_EXE=.venv\Scripts\python.exe"

:INSTALL_DEPS
echo [2/3] Verifying and installing required packages...
"%PYTHON_EXE%" -m pip install -q --disable-pip-version-check -e .
if %errorlevel% neq 0 (
    echo [WARNING] Package installation returned non-zero code. Attempting to launch anyway...
)

:RUN_VECTRA
echo [3/3] Starting Vectra Desktop IDE...
echo =========================================================================
echo.

"%PYTHON_EXE%" -m kheramat.gui.app

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Vectra exited with error code: %errorlevel%
    echo Log file created at: %USERPROFILE%\.vectra\logs\vectra_app.log
    pause
)
