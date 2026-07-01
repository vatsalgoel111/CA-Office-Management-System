"""
File Purpose: Integration tests for SQLite database initialization.
Module: tests.integration.test_database_initializer
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: pathlib, sqlite3, sys, tempfile, unittest, unittest.mock.
"""

from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from app.config import load_config  # noqa: E402
from app.core.paths import build_paths, ensure_runtime_directories  # noqa: E402
from app.database.connection import create_connection_manager  # noqa: E402
from app.database.initializer import (  # noqa: E402
    check_database_integrity,
    initialize_database,
)


class DatabaseInitializerTest(unittest.TestCase):
    """Tests for schema creation and required seed data."""

    def test_initialize_database_creates_schema_and_seed_data(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env = {"CA_CMS_RUNTIME_ROOT": temp_dir}
            with patch.dict("os.environ", env, clear=True):
                config = load_config(project_root=PROJECT_ROOT)

            paths = build_paths(config)
            ensure_runtime_directories(paths)
            connection_manager = create_connection_manager(config, paths)
            initialize_database(connection_manager, paths)

            self.assertTrue(paths.database_file.exists())
            self.assertTrue(check_database_integrity(connection_manager))

            with connection_manager.connect() as connection:
                table_count = connection.execute(
                    "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table';"
                ).fetchone()[0]
                role_count = connection.execute(
                    "SELECT COUNT(*) FROM roles;"
                ).fetchone()[0]
                permission_count = connection.execute(
                    "SELECT COUNT(*) FROM permissions;"
                ).fetchone()[0]

            self.assertGreaterEqual(table_count, 14)
            self.assertEqual(role_count, 5)
            self.assertEqual(permission_count, 15)


if __name__ == "__main__":
    unittest.main()

