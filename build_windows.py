import os
import sys
import subprocess
import shutil
import zipfile

def build_executable():
    print("============================================================")
    print("         VECTRA STANDALONE WINDOWS BUILD ENGINE            ")
    print("============================================================")

    # 1. Ensure ICO asset exists
    if not os.path.exists("Vectra.ico"):
        print("[1/5] Generating Vectra.ico from Vectra.png...")
        from PIL import Image
        img = Image.open("Vectra.png")
        img.save("Vectra.ico", format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    else:
        print("[1/5] Vectra.ico asset verified.")

    # 2. Run PyInstaller
    print("[2/5] Compiling standalone executable via PyInstaller...")
    cmd = [sys.executable, "-m", "PyInstaller", "--noconfirm", "Vectra.spec"]
    res = subprocess.run(cmd)
    if res.returncode != 0:
        print("ERROR: PyInstaller build failed!")
        sys.exit(1)

    # 3. Create Portable Zip
    print("[3/5] Creating Vectra-0.1.0-Portable.zip...")
    dist_dir = os.path.join("dist", "Vectra")
    zip_path = os.path.join("dist", "Vectra-0.1.0-Portable.zip")

    if os.path.exists(zip_path):
        os.remove(zip_path)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(dist_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, dist_dir)
                zipf.write(abs_path, os.path.join("Vectra", rel_path))

    print(f"Portable archive created: {zip_path}")

    # 4. Generate Inno Setup Script if ISCC exists
    iscc_path = shutil.which("iscc") or r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    if os.path.exists(iscc_path):
        print("[4/5] Compiling Vectra-0.1.0-Setup.exe via Inno Setup...")
        iss_content = f'''
[Setup]
AppName=Vectra
AppVersion=0.1.0
AppPublisher=Under Protocol Industry Software Solutions
DefaultDirName={{autopf}}\\Vectra
DefaultGroupName=Vectra
UninstallDisplayIcon={{app}}\\Vectra.exe
Compression=lzma2
SolidCompression=yes
OutputDir=dist
OutputBaseFilename=Vectra-0.1.0-Setup
SetupIconFile=Vectra.ico

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"

[Files]
Source: "dist\\Vectra\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{group}}\\Vectra"; Filename: "{{app}}\\Vectra.exe"
Name: "{{group}}\\Uninstall Vectra"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\Vectra"; Filename: "{{app}}\\Vectra.exe"; Tasks: desktopicon
'''
        with open("Vectra_Setup.iss", "w", encoding="utf-8") as f:
            f.write(iss_content)
        subprocess.run([iscc_path, "Vectra_Setup.iss"])
    else:
        print("[4/5] Inno Setup compiler (ISCC) not found in system PATH. Skipping installer EXE creation.")

    print("[5/5] Build process completed successfully.")

if __name__ == "__main__":
    build_executable()

