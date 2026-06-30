"""
File Purpose: Developer script for checking local database health.
Module: scripts.check_database
Author: CA Office CMS Development Team
Created Date: 2026-07-01
Last Modified: 2026-07-01
Dependencies: pathlib, sqlite3, sys.
"""

from pathlib import Path
import sqlite3
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_FILE = PROJECT_ROOT / "data" / "ca_office_cms.sqlite3"


def main() -> int:
    """Print basic database health information."""

    if not DATABASE_FILE.exists():
        print(f"Database not found: {DATABASE_FILE}")
        return 1

    connection = sqlite3.connect(str(DATABASE_FILE))
    try:
        integrity = connection.execute("PRAGMA integrity_check;").fetchone()[0]
        table_count = connection.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table';"
        ).fetchone()[0]
        role_count = connection.execute("SELECT COUNT(*) FROM roles;").fetchone()[0]
        permission_count = connection.execute(
            "SELECT COUNT(*) FROM permissions;"
        ).fetchone()[0]
        role_permission_count = connection.execute(
            "SELECT COUNT(*) FROM role_permissions;"
        ).fetchone()[0]
    finally:
        connection.close()

    print(f"Integrity: {integrity}")
    print(f"Tables: {table_count}")
    print(f"Roles: {role_count}")
    print(f"Permissions: {permission_count}")
    print(f"Role permissions: {role_permission_count}")
    return 0 if integrity == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())

