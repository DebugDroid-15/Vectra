@echo off
setlocal enabledelayedexpansion
title Vectra - Scientific Computing Desktop Environment

echo =========================================================================
echo                   Vectra Desktop Scientific Computing
echo =========================================================================
echo Launching Vectra... Please wait.
echo.

set "PYTHON_EXE="

:: 1. Check local virtual environment (.venv)
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
    echo [INFO] Found local virtual environment at .venv
    goto :FOUND
)

:: 2. Try 'py' launcher (standard Windows Python launcher installed with official Python)
py -c "import sys; print(sys.version)" >nul 2>&1
if !errorlevel! equ 0 (
    set "PYTHON_EXE=py"
    echo [INFO] Detected Python via Windows 'py' launcher
    goto :FOUND
)

:: 3. Try system 'python' command (ensuring it's not the Windows Store 0-byte stub)
python -c "import sys; print(sys.version)" >nul 2>&1
if !errorlevel! equ 0 (
    set "PYTHON_EXE=python"
    echo [INFO] Detected Python from system PATH
    goto :FOUND
)

:: 4. Try system 'python3' command
python3 -c "import sys; print(sys.version)" >nul 2>&1
if !errorlevel! equ 0 (
    set "PYTHON_EXE=python3"
    echo [INFO] Detected python3 from system PATH
    goto :FOUND
)

:: 5. Auto-scan all standard Python installation directories across user profile & system drives
for /d %%D in ("%LocalAppData%\Programs\Python\Python*") do (
    if exist "%%D\python.exe" (
        "%%D\python.exe" -c "import sys; print(sys.version)" >nul 2>&1
        if !errorlevel! equ 0 (
            set "PYTHON_EXE=%%D\python.exe"
            echo [INFO] Detected Python at %%D\python.exe
            goto :FOUND
        )
    )
)

for /d %%D in ("C:\Python*") do (
    if exist "%%D\python.exe" (
        "%%D\python.exe" -c "import sys; print(sys.version)" >nul 2>&1
        if !errorlevel! equ 0 (
            set "PYTHON_EXE=%%D\python.exe"
            echo [INFO] Detected Python at %%D\python.exe
            goto :FOUND
        )
    )
)

for /d %%D in ("C:\Program Files\Python*") do (
    if exist "%%D\python.exe" (
        "%%D\python.exe" -c "import sys; print(sys.version)" >nul 2>&1
        if !errorlevel! equ 0 (
            set "PYTHON_EXE=%%D\python.exe"
            echo [INFO] Detected Python at %%D\python.exe
            goto :FOUND
        )
    )
)

for /d %%D in ("%ProgramFiles%\Python*") do (
    if exist "%%D\python.exe" (
        "%%D\python.exe" -c "import sys; print(sys.version)" >nul 2>&1
        if !errorlevel! equ 0 (
            set "PYTHON_EXE=%%D\python.exe"
            echo [INFO] Detected Python at %%D\python.exe
            goto :FOUND
        )
    )
)

for /d %%D in ("%ProgramData%\Anaconda3*" "%ProgramData%\Miniconda3*" "%UserProfile%\Anaconda3*" "%UserProfile%\Miniconda3*") do (
    if exist "%%D\python.exe" (
        "%%D\python.exe" -c "import sys; print(sys.version)" >nul 2>&1
        if !errorlevel! equ 0 (
            set "PYTHON_EXE=%%D\python.exe"
            echo [INFO] Detected Python Conda environment at %%D\python.exe
            goto :FOUND
        )
    )
)

:NOT_FOUND
echo =========================================================================
echo [ERROR] No working Python installation was found on this system!
echo =========================================================================
echo.
echo Windows requires Python to be installed. Please install Python 3.10+:
echo 1. Download Python from: https://www.python.org/downloads/
echo 2. Check the box "Add python.exe to PATH" during installation!
echo.
pause
exit /b 9009

:FOUND
echo =========================================================================
echo [1/2] Verifying and installing required packages...
"%PYTHON_EXE%" -m pip install -q --disable-pip-version-check -e .
if %errorlevel% neq 0 (
    echo [WARNING] Package installation returned non-zero code. Attempting to launch anyway...
)

echo [2/2] Starting Vectra Desktop IDE...
echo =========================================================================
echo.

"%PYTHON_EXE%" -m kheramat.gui.app

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Vectra exited with error code: %errorlevel%
    echo Log file created at: %USERPROFILE%\.vectra\logs\vectra_app.log
    pause
)
