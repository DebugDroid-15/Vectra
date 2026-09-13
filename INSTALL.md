# VECTRA — Installation & User Execution Guide

Welcome to **Vectra**, an independent, open-source scientific computing and engineering desktop environment. This guide provides step-by-step instructions for installing, configuring, running, and troubleshooting Vectra across Windows, Linux, and macOS platforms.

---

## 🚀 1. One-Click Quick Start (Windows)

For Windows users, Vectra includes a zero-configuration automated launcher script (`Vectra.bat`) that scans system dependencies, initializes an isolated virtual environment, installs graphical and scientific libraries with live progress feedback, and launches the desktop environment.

### Steps:
1. **Download / Clone Repository**:
   ```cmd
   git clone https://github.com/DebugDroid-15/Vectra.git
   cd Vectra
   ```
2. **Double-Click or Run `Vectra.bat`**:
   ```cmd
   Vectra.bat
   ```

### What `Vectra.bat` Does Automatically:
* 🔍 **System Scan**: Automatically detects standard Python installations (`py` launcher, system `PATH`, LocalAppData, Program Files, Conda/Anaconda).
* ⚙️ **Directory Inspection**: Verifies write permissions and checks local workspace paths.
* 📊 **Progress & ETA Display**: Shows a live progress percentage bar with an estimated time remaining (ETA) countdown so you know installation is actively proceeding.
* 📦 **Virtual Environment (.venv)**: Initializes an isolated Python environment to avoid polluting global or system packages.
* 🛠️ **Dependency Binding**: Installs PySide6, NumPy, Matplotlib, SciPy, SymPy, and registers Vectra in editable mode.
* 🖥️ **GUI Launch**: Runs `python -m kheramat.gui.app` directly.

---

## 🐧 2. Linux & macOS Installation Guide

### Prerequisites:
* **Python**: Python 3.10 or newer.

### Steps:
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/DebugDroid-15/Vectra.git
   cd Vectra
   ```

2. **Create & Activate Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies & Package**:
   ```bash
   pip install --upgrade pip
   pip install -e .
   ```

4. **Launch Desktop Application**:
   ```bash
   python3 -m kheramat.gui.app
   ```

---

## 💻 3. Running Headless (Command Line / Server Execution)

Vectra includes a standalone CLI utility (`vectra-cli`) for running computations without launching the graphical desktop interface:

### Evaluate Expression Headlessly:
```bash
vectra-cli --eval "A = [1 2; 3 4]; B = A * 2; disp(B);"
```

### Run Script File Headlessly:
```bash
vectra-cli --run path/to/script.m
```

---

## 🔧 4. Troubleshooting & FAQ

### Issue: "No compatible Python installation was found"
* **Cause**: Python is either not installed or was not added to your system `PATH`.
* **Fix**:
  1. Download Python 3.10+ from [python.org](https://www.python.org/downloads/).
  2. During installation, **ensure you check the box**: `"Add python.exe to PATH"`.
  3. Re-run `Vectra.bat`.

### Issue: "DLL load failed while importing QtWidgets" (Conda / Anaconda Users)
* **Cause**: PATH conflicts between Anaconda Qt binaries and PySide6.
* **Fix**: `Vectra.bat` handles this automatically by setting isolated DLL search paths. If running manually in Anaconda prompt, ensure you run inside an isolated `.venv`.

### Log File Location:
If Vectra crashes unexpectedly, full diagnostic traces are automatically logged to:
* **Windows**: `%USERPROFILE%\.vectra\logs\vectra_app.log`
* **Linux/macOS**: `~/.vectra/logs/vectra_app.log`

