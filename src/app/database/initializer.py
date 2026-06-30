"""
File Purpose: Database schema and seed initialization.
Module: app.database.initializer
Author: CA Office CMS Development Team
Created Date: 2026-07-01
Last Modified: 2026-07-01
Dependencies: pathlib, app.database.connection, app.core.exceptions, app.core.paths.
"""

from pathlib import Path

from app.core.exceptions import DatabaseError
from app.core.paths import AppPaths
from app.database.connection import DatabaseConnectionManager


def _read_sql_file(file_path: Path) -> str:
    try:
        return file_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise DatabaseError(f"Unable to read SQL file {file_path}: {exc}") from exc


def initialize_database(
    connection_manager: DatabaseConnectionManager,
    paths: AppPaths,
) -> None:
    """Create database schema and seed required system data."""

    schema_file = paths.project_root / "src" / "app" / "database" / "schema.sql"
    seed_file = paths.project_root / "src" / "app" / "database" / "seed.sql"
    schema_sql = _read_sql_file(schema_file)
    seed_sql = _read_sql_file(seed_file)

    try:
        with connection_manager.transaction() as connection:
            connection.executescript(schema_sql)
            connection.executescript(seed_sql)
    except Exception as exc:
        raise DatabaseError(f"Database initialization failed: {exc}") from exc


def check_database_integrity(
    connection_manager: DatabaseConnectionManager,
) -> bool:
    """Run a SQLite integrity check for the current database."""

    try:
        with connection_manager.connect() as connection:
            result = connection.execute("PRAGMA integrity_check;").fetchone()
            return bool(result and result[0] == "ok")
    except Exception as exc:
        raise DatabaseError(f"Database integrity check failed: {exc}") from exc

