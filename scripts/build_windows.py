"""
File Purpose: Build Windows executable using PyInstaller.
Module: scripts.build_windows
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: pathlib, subprocess, sys.
"""

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SPEC_FILE = PROJECT_ROOT / "packaging" / "CAOfficeCMS.spec"


def main() -> int:
    """Build the Windows executable from the PyInstaller spec."""

    if not SPEC_FILE.exists():
        print(f"Missing PyInstaller spec: {SPEC_FILE}")
        return 1

    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        str(SPEC_FILE),
    ]
    result = subprocess.run(command, cwd=PROJECT_ROOT, check=False)
    return int(result.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
