# VECTRA — INSTALLATION & SETUP GUIDE

```
  ___ ___ ____________ ________ _________    _____   
 /   |   \\______   \\_____  \\______   \  /  _  \  
/    ~    \|    |  _/ /   |   \|    |  _/ /  /_\  \ 
\    Y    /|    |   \/    |    \    |   \/    |    \
 \___|_  / |______  /\_______  /______  /\____|__  /
       \/         \/         \/       \/         \/ 
```

**Official Attribution:**  
*Made by Amar Khera / Under Protocol Industry Software Solutions*  
*License: MIT*

---

## 📋 Prerequisites

To run **Vectra**, your system must satisfy:
- **Operating System**: Windows 10/11, macOS (10.15+), or Linux (Ubuntu 20.04+, Debian, Fedora, Arch).
- **Python**: Python 3.10, 3.11, or 3.12 installed on your machine.
- **Git**: Installed and accessible via command line.

---

## ⚡ Option 1: Automatic 1-Click Launch (Windows)

If you are on Windows, you do **not** need to manually configure virtual environments or install Python packages. The included automated launcher script (`Vectra.bat`) will set everything up for you automatically.

1. **Clone the Repository**:
   ```cmd
   git clone https://github.com/DebugDroid-15/Vectra.git
   cd Vectra
   ```

2. **Run `Vectra.bat`**:
   Double-click `Vectra.bat` in Windows Explorer or execute it from PowerShell/CMD:
   ```cmd
   .\Vectra.bat
   ```

`Vectra.bat` automatically:
- Checks for an available Python installation (`python`).
- Initializes a local isolated virtual environment (`.venv`).
- Installs all engineering dependencies (`PySide6`, `NumPy`, `SciPy`, `SymPy`, `Matplotlib`).
- Launches the complete **Vectra Desktop Application**.

---

## 🛠️ Option 2: Manual Installation (Windows, Linux, macOS)

If you prefer installing Vectra into a custom environment or are using Linux/macOS:

### Step 1: Clone the Repository
```bash
git clone https://github.com/DebugDroid-15/Vectra.git
cd Vectra
```

### Step 2: Create & Activate Virtual Environment
```bash
# On Linux / macOS:
python3 -m venv .venv
source .venv/bin/activate

# On Windows (PowerShell):
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Required Dependencies
```bash
pip install -e .
```
*(Or install core dependencies manually: `pip install PySide6 numpy scipy sympy matplotlib pytest`)*

### Step 4: Launch Vectra

- **GUI Mode (Desktop App)**:
  ```bash
  python -m kheramat.gui.app
  ```

- **Headless Command Line REPL**:
  ```bash
  python -m kheramat.cli
  ```

- **Run Script File directly**:
  ```bash
  python -m kheramat.cli --run tests/regression/VECTRA_EXTENDED_SYSTEM_TEST.m
  ```

---

## 🧪 Option 3: Running the Full Test & Verification Suite

To verify that all mathematical engine toolboxes, DSP functions, linear algebra solvers, symbolic differentiators, and GUI controls are 100% operational on your machine:

```bash
python -m pytest tests
```

Expected output:
```
40 passed in 6.97s
```

---

## ❓ Troubleshooting & Support

| Issue | Cause | Resolution |
| :--- | :--- | :--- |
| `python: command not found` | Python is not added to System PATH | Install Python 3.11 from [python.org](https://www.python.org/) and check *"Add Python to PATH"* during installation. |
| `qt.qpa.plugin: Could not load the Qt platform plugin "xcb"` *(Linux)* | Missing X11/xcb libraries | Run `sudo apt install libxcb-cursor0 libxcb-xinerama0 libxcb-icccm4` on Debian/Ubuntu systems. |
| `ImportError: PySide6` | Virtual environment not activated | Ensure `.venv` is activated (`source .venv/bin/activate` or `.\.venv\Scripts\activate`) before running. |
