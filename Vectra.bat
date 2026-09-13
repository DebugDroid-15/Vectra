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

:: 1. Check local virtualenv first
if exist ".venv\Scripts\python.exe" (
    set "SYS_PYTHON=.venv\Scripts\python.exe"
    goto :FOUND_PYTHON
)

:: 2. Try Windows 'py' launcher
py -3 -c "import sys" >nul 2>&1
if !errorlevel! equ 0 (
    set "SYS_PYTHON=py -3"
    goto :FOUND_PYTHON
)

:: 3. Try standard python executable
python -c "import sys" >nul 2>&1
if !errorlevel! equ 0 (
    set "SYS_PYTHON=python"
    goto :FOUND_PYTHON
)

:: 4. Auto-scan standard local installation folders
for /d %%D in ("%LocalAppData%\Programs\Python\Python*") do (
    if exist "%%D\python.exe" (
        "%%D\python.exe" -c "import sys" >nul 2>&1
        if !errorlevel! equ 0 (
            set "SYS_PYTHON=%%D\python.exe"
            goto :FOUND_PYTHON
        )
    )
)

for /d %%D in ("C:\Python*") do (
    if exist "%%D\python.exe" (
        "%%D\python.exe" -c "import sys" >nul 2>&1
        if !errorlevel! equ 0 (
            set "SYS_PYTHON=%%D\python.exe"
            goto :FOUND_PYTHON
        )
    )
)

for /d %%D in ("C:\Program Files\Python*") do (
    if exist "%%D\python.exe" (
        "%%D\python.exe" -c "import sys" >nul 2>&1
        if !errorlevel! equ 0 (
            set "SYS_PYTHON=%%D\python.exe"
            goto :FOUND_PYTHON
        )
    )
)

:NOT_FOUND
echo.
echo =========================================================================
echo [ERROR] No Python 3.10+ installation was found!
echo Please install Python from https://www.python.org/downloads/
echo Make sure to check "Add python.exe to PATH" during installation.
echo =========================================================================
echo.
pause
exit /b 9009

:FOUND_PYTHON
echo [1/3] Running Vectra Environment Setup Wizard...
%SYS_PYTHON% src\kheramat\setup_wizard.py

:: Determine executable path
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
) else (
    set "PYTHON_EXE=%SYS_PYTHON%"
)

echo.
echo [2/3] Verifying core graphical packages...
%PYTHON_EXE% -c "import PySide6, numpy, matplotlib" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing required dependencies...
    %PYTHON_EXE% -m pip install PySide6 numpy matplotlib scipy sympy -e .
)

echo.
echo [3/3] Launching Vectra GUI Application...
echo =========================================================================
echo.

%PYTHON_EXE% -m kheramat.gui.app

if %errorlevel% neq 0 (
    echo.
    echo =========================================================================
    echo [ERROR] Vectra exited with error code: %errorlevel%
    echo =========================================================================
    pause
)


