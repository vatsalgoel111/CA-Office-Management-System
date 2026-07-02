# Installation Guide

This document will be updated step by step as tools become necessary.

We will not install every tool at once. Each tool will be installed only when the project reaches the point where it is needed.

## Required Tools Over the Project Lifetime

### Python

Needed for application development and execution.

### Git

Needed for version control and GitHub collaboration.

### VS Code

Optional but recommended for editing and debugging.

### DB Browser for SQLite

Optional but useful for inspecting the SQLite database during development.

### Python Packages

The project uses a dedicated virtual environment named `.venv`.

Create it from the project root if it does not already exist:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install runtime dependencies:

```powershell
pip install -r requirements.txt
```

Verify CustomTkinter:

```powershell
python -c "import customtkinter; print(customtkinter.__version__)"
```

Run automated tests:

```powershell
python scripts\run_tests.py
```

Currently required runtime packages:

- CustomTkinter

Development packaging packages:

- PyInstaller

Install packaging dependencies only on the build machine:

```powershell
pip install -r requirements-dev.txt
```

Verify PyInstaller:

```powershell
python -m PyInstaller --version
```

Planned future packages:

- OpenPyXL
- ReportLab
- Matplotlib
- pytest

## Virtual Environment Rules

- Use `.venv` for project commands.
- Do not commit `.venv`.
- Run Python commands through the virtual environment during development.
- If a dependency is needed, add it to `requirements.txt` before relying on it in source code.

## Installation Workflow

For each required installation, we will document:

- Why it is needed
- Official download source
- Installation steps
- Recommended options
- Common mistakes
- Verification command
