# Packaging

This folder contains the PyInstaller build specification for Version 1.0.

## Build Executable

Install development packaging dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Build:

```powershell
.\.venv\Scripts\python.exe scripts\build_windows.py
```

Expected output:

```text
dist\CAOfficeCMS\CAOfficeCMS.exe
```

The application stores runtime database, backups, exports, and logs outside the executable folder according to runtime configuration.
