"""
File Purpose: Unit tests for configuration and path management.
Module: tests.unit.test_config_and_paths
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: os, pathlib, sys, tempfile, unittest, unittest.mock.
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
from app.constants import DatabaseProvider, Environment, LogLevel  # noqa: E402
from app.core.paths import build_paths, ensure_runtime_directories  # noqa: E402


class ConfigAndPathsTest(unittest.TestCase):
    """Tests for environment-aware config and runtime paths."""

    def test_load_config_uses_safe_defaults(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            config = load_config(project_root=PROJECT_ROOT)

        self.assertEqual(config.environment, Environment.DEVELOPMENT)
        self.assertEqual(config.database_provider, DatabaseProvider.SQLITE)
        self.assertEqual(config.log_level, LogLevel.DEBUG)
        self.assertTrue(config.debug)

    def test_load_config_reads_environment_overrides(self) -> None:
        env = {
            "CA_CMS_ENV": "production",
            "CA_CMS_DB_PROVIDER": "sqlite",
            "CA_CMS_DB_NAME": "office.sqlite3",
            "CA_CMS_LOG_LEVEL": "WARNING",
            "CA_CMS_DEBUG": "false",
        }
        with patch.dict("os.environ", env, clear=True):
            config = load_config(project_root=PROJECT_ROOT)

        self.assertEqual(config.environment, Environment.PRODUCTION)
        self.assertEqual(config.database_name, "office.sqlite3")
        self.assertEqual(config.log_level, LogLevel.WARNING)
        self.assertFalse(config.debug)

    def test_ensure_runtime_directories_creates_expected_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env = {"CA_CMS_RUNTIME_ROOT": temp_dir}
            with patch.dict("os.environ", env, clear=True):
                config = load_config(project_root=PROJECT_ROOT)

            paths = build_paths(config)
            ensure_runtime_directories(paths)

            self.assertTrue(paths.data_dir.exists())
            self.assertTrue(paths.backups_dir.exists())
            self.assertTrue(paths.excel_exports_dir.exists())
            self.assertTrue(paths.pdf_exports_dir.exists())
            self.assertTrue(paths.logs_dir.exists())


if __name__ == "__main__":
    unittest.main()

