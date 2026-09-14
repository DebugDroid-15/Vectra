import os
import sys
import zipfile
import shutil

def build_dist():
    print("Creating Vectra portable release layout...")
    if os.path.exists("dist"):
        try:
            shutil.rmtree("dist")
        except Exception:
            pass
            
    dist_dir = os.path.join("dist", "Vectra")
    os.makedirs(dist_dir, exist_ok=True)
    
    # Copy source files excluding .venv and __pycache__
    src_target = os.path.join(dist_dir, "src")
    shutil.copytree("src", src_target, ignore=shutil.ignore_patterns(".venv", "__pycache__", "*.pyc", "*~*"))
    
    # Copy root assets
    for asset in ["Vectra.png", "Vectra.ico", "README.md"]:
        if os.path.exists(asset):
            shutil.copy(asset, dist_dir)
            
    # Create embedded launcher batch script
    cmd_launcher = os.path.join(dist_dir, "Vectra.bat")
    with open(cmd_launcher, "w", encoding="utf-8") as f:
        f.write("@echo off\n")
        f.write("set PYTHONPATH=%~dp0src\n")
        f.write("python -m kheramat.gui.app %*\n")
        
    # Create portable zip
    zip_path = os.path.join("dist", "Vectra-0.1.0-Portable.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(dist_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, dist_dir)
                zipf.write(abs_path, os.path.join("Vectra", rel_path))
                
    print("Vectra portable release created successfully at:", zip_path)

if __name__ == "__main__":
    build_dist()

