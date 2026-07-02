# Windows Installer

This folder contains the Inno Setup script for building the Version 1.0 Windows installer.

## Required Tool

Inno Setup is free and open source.

Official source:

```text
https://jrsoftware.org/isinfo.php
```

## Build Order

1. Build the PyInstaller executable.
2. Open `installer\CAOfficeCMS.iss` in Inno Setup Compiler.
3. Compile the installer.

Expected output:

```text
dist\installer\CAOfficeCMSSetup-1.0.0.exe
```

Do not build the installer until `dist\CAOfficeCMS\CAOfficeCMS.exe` exists.
