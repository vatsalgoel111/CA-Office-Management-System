"""
File Purpose: Run release preflight checks for deployment readiness.
Module: scripts.release_preflight
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: pathlib, subprocess, sys.
"""

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> int:
    """Run a command from the project root."""

    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command, cwd=PROJECT_ROOT, check=False)
    return int(result.returncode)


def main() -> int:
    """Run compile, test, and database checks."""

    commands = [
        [sys.executable, "-m", "compileall", "src", "scripts", "tests"],
        [sys.executable, "scripts/run_tests.py"],
        [sys.executable, "scripts/check_database.py"],
    ]
    for command in commands:
        exit_code = run(command)
        if exit_code != 0:
            return exit_code
    print("Release preflight checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
