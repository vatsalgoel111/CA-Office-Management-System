# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Directory containing this spec file
SPEC_DIR = SPECPATH

# Project root (one level above the packaging folder)
PROJECT_ROOT = os.path.abspath(os.path.join(SPEC_DIR, ".."))

customtkinter_datas = collect_data_files("customtkinter")

app_datas = [
    (os.path.join(PROJECT_ROOT, "src", "app", "database", "schema.sql"), "app/database"),
    (os.path.join(PROJECT_ROOT, "src", "app", "database", "seed.sql"), "app/database"),
]

a = Analysis(
    [os.path.join(PROJECT_ROOT, "src", "app", "main.py")],
    pathex=[os.path.join(PROJECT_ROOT, "src")],
    binaries=[],
    datas=customtkinter_datas + app_datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="CAOfficeCMS",
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    name="CAOfficeCMS",
)