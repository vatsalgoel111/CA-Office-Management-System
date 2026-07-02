# CA Office Management System

Production-focused Windows desktop software for managing Chartered Accountant office workflows.

## Project Status

Current phase: Version 1.0 production deployment preparation.

Completed Version 1.0 foundations:

- Login and role-based access
- Dashboard
- Client, staff, work, billing, and collection management
- Reports with CSV export
- Audit log
- Verified SQLite backups
- Reminder foundation
- Notification and WhatsApp queue foundation
- Settings
- Reusable professional UI foundation
- Automated integration and unit tests

## Version Goal

Version 1.0 will replace the office's shared Excel workflow with a structured desktop application backed by SQLite. Excel will be used only for importing existing data and exporting reports.

## Technology Stack

- Python
- CustomTkinter
- SQLite
- OpenPyXL
- ReportLab
- Matplotlib
- PyInstaller
- Git and GitHub

All selected technologies are free and open source.

## Development Rule

Each module follows this workflow:

1. Planning
2. Architecture
3. Core foundation when needed
4. Database
5. UI foundation or design
6. Implementation
7. Testing
8. Improvements
9. Git Commit

We complete and test one module before moving to the next.

## Documentation

Primary project documents are maintained in the `docs/` folder.

## Development Commands

Use the dedicated virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run tests:

```powershell
python scripts\run_tests.py
```

Check database health:

```powershell
python scripts\check_database.py
```

Run release preflight:

```powershell
python scripts\release_preflight.py
```

Build Windows executable after installing development packaging dependencies:

```powershell
python scripts\build_windows.py
```
