# How to Run Vectra — Execution & Installation Guide

This guide provides step-by-step instructions for running **Vectra** on Windows, Linux, and macOS platforms.

---

## 📋 System Requirements

- **Operating System**: Windows 10/11, Ubuntu 20.04+, or macOS 11+
- **Python**: Python 3.10, 3.11, or 3.12 installed on your system.
- **Git**: (Optional) For cloning the repository.

---

## 🪟 Method 1: 1-Click Launch on Windows (Recommended for Windows Users)

If you are using Windows, running Vectra requires no manual terminal configuration:

1. **Download or Clone the Repository**:
   - Download the `.zip` archive from [GitHub](https://github.com/DebugDroid-15/Vectra) and extract it, or run:
     ```cmd
     git clone https://github.com/DebugDroid-15/Vectra.git
     ```
2. **Double-Click `Vectra.bat`**:
   - Navigate into the `Vectra` folder.
   - Double-click **`Vectra.bat`**.

> **What `Vectra.bat` does automatically:**
> - Checks if Python is installed and added to `PATH`.
> - Creates a clean virtual environment (`.venv`) if one does not exist.
> - Installs all necessary dependencies (`NumPy`, `SciPy`, `SymPy`, `Matplotlib`, `PySide6`).
> - Launches the Vectra splash screen and main desktop application automatically.

---

## 💻 Method 2: Running from Terminal (Cross-Platform: Windows, Linux, macOS)

### Step 1: Clone the Repository
```bash
git clone https://github.com/DebugDroid-15/Vectra.git
cd Vectra
```

### Step 2: Create & Activate Virtual Environment

- **On Windows (PowerShell / Command Prompt)**:
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\activate
  ```

- **On Linux / macOS**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### Step 3: Install Dependencies
Install Vectra in editable mode along with required scientific stack libraries:
```bash
pip install -e .
```

### Step 4: Launch the Desktop IDE
```bash
python -m kheramat.gui.app
```

---

## 🧪 Method 3: Running Automated Tests

Vectra includes a complete unit test suite covering matrix commands, parser nodes, ECE toolboxes, help documentation, and logger handlers.

To run tests:
```bash
# Install pytest if not already installed
pip install pytest

# Execute all tests
pytest tests/
```

---

## ❓ Troubleshooting & FAQs

### 1. `ModuleNotFoundError: No module named 'PySide6'`
Ensure you have activated your virtual environment (`source .venv/bin/activate` or `.\.venv\Scripts\activate`) and executed `pip install -e .`.

### 2. Qt Platform Plugin Errors on Linux
On headless or minimal Linux installations, Qt requires standard x11/xcb libraries:
```bash
sudo apt-get update
sudo apt-get install -y libxcb-xinerama0 libxcb-cursor0 libdbus-1-3
```

### 3. Viewing Logs & Crash Reports
If an unexpected crash or warning occurs:
- Open Vectra and click **"📋 Logs & Crashes"** on the main top toolbar.
- Alternatively, check the log files located in your user directory:
  - Windows: `%USERPROFILE%\.vectra\logs\vectra_app.log`
  - Linux/macOS: `~/.vectra/logs/vectra_app.log`
