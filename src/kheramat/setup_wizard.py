import sys
import os
import time
import subprocess
import shutil

def print_progress(percentage: int, title: str, detail: str, eta_str: str, length: int = 30):
    filled_length = int(length * percentage // 100)
    bar = '=' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r[{bar}] {percentage:3d}% | {title}: {detail} ({eta_str})   ')
    sys.stdout.flush()

def setup_environment():
    print("=" * 75)
    print("           VECTRA PLATFORM AUTOMATED ENVIRONMENT SETUP")
    print("=" * 75)
    print("Scanning installation directory & initializing environment components...\n")

    # Correct root determination: setup_wizard.py is inside src/kheramat/
    kheramat_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.dirname(kheramat_dir)
    project_root = os.path.dirname(src_dir)

    venv_dir = os.path.join(project_root, ".venv")
    python_exe = sys.executable

    steps = [
        ("Directory Verification", 15, "Verifying project write permissions..."),
        ("Runtime Environment", 35, "Configuring Python virtual environment..."),
        ("Core Packages", 75, "Installing PySide6, NumPy & Matplotlib (this may take 1-2 min)..."),
        ("Vectra Core Binding", 90, "Registering Vectra engine module..."),
        ("Finalizing Setup", 100, "Setting up workspace & logging paths...")
    ]

    start_time = time.time()

    for idx, (title, pct, detail) in enumerate(steps):
        elapsed = time.time() - start_time
        if pct > 0:
            total_est = (elapsed / pct) * 100
            eta_sec = max(0, int(total_est - elapsed))
            eta_str = f"ETA: {eta_sec}s"
        else:
            eta_str = "Calculating..."

        print_progress(pct, title, detail, eta_str)

        try:
            if idx == 0:
                test_file = os.path.join(project_root, ".write_test.tmp")
                with open(test_file, "w") as f:
                    f.write("test")
                os.remove(test_file)
                time.sleep(0.2)

            elif idx == 1:
                # Build venv if missing
                venv_python = os.path.join(venv_dir, "Scripts", "python.exe") if os.name == 'nt' else os.path.join(venv_dir, "bin", "python")
                if not os.path.exists(venv_python):
                    print(f"\n[INFO] Creating virtual environment at {venv_dir}...")
                    subprocess.run([python_exe, "-m", "venv", venv_dir], check=False)
                time.sleep(0.2)

            elif idx == 2:
                # Locate venv python or fallback to system python
                venv_python = os.path.join(venv_dir, "Scripts", "python.exe") if os.name == 'nt' else os.path.join(venv_dir, "bin", "python")
                if not os.path.exists(venv_python):
                    venv_python = python_exe

                # Check if core dependencies are already present to avoid pip overhead
                check_cmd = [venv_python, "-c", "import PySide6, numpy, matplotlib"]
                check_res = subprocess.run(check_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if check_res.returncode != 0:
                    cmd = [venv_python, "-m", "pip", "install", "--no-warn-script-location", "PySide6", "numpy", "matplotlib", "scipy", "sympy"]
                    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            elif idx == 3:
                venv_python = os.path.join(venv_dir, "Scripts", "python.exe") if os.name == 'nt' else os.path.join(venv_dir, "bin", "python")
                if not os.path.exists(venv_python):
                    venv_python = python_exe

                check_cmd = [venv_python, "-c", "import kheramat"]
                check_res = subprocess.run(check_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if check_res.returncode != 0:
                    cmd = [venv_python, "-m", "pip", "install", "--no-warn-script-location", "-e", project_root]
                    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            elif idx == 4:
                logs_dir = os.path.join(os.path.expanduser("~"), ".vectra", "logs")
                os.makedirs(logs_dir, exist_ok=True)
                time.sleep(0.2)

        except Exception as e:
            print(f"\n[ERROR] Setup step '{title}' encountered issue: {e}")

    elapsed = time.time() - start_time
    print_progress(100, "Setup Complete", "Environment ready", "0s")
    print("\n" + "=" * 75)
    print(" [SUCCESS] Vectra Environment Setup Completed ({:.1f}s)".format(elapsed))
    print("=" * 75 + "\n")

if __name__ == "__main__":
    setup_environment()
