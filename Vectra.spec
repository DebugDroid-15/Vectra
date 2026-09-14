# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/kheramat/gui/app.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        ('Vectra.png', '.'),
        ('Vectra.ico', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'PySide6',
        'numpy',
        'scipy',
        'sympy',
        'matplotlib',
        'kheramat',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['torch', 'pytest', 'pycparser', 'nltk', 'sklearn', 'pandas', 'tensorflow', 'cv2'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Vectra',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='Vectra.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Vectra',
)
