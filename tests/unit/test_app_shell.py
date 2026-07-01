"""
File Purpose: Unit tests for application shell routing metadata.
Module: tests.unit.test_app_shell
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: pathlib, sys, unittest.
"""

from pathlib import Path
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from app.app_shell import ApplicationShell  # noqa: E402
from app.constants import PermissionCode  # noqa: E402
from app.ui.app_shell import AppShell  # noqa: E402


class AppShellTest(unittest.TestCase):
    """Tests for app shell route metadata without opening windows."""

    def test_application_shell_route_names(self) -> None:
        self.assertEqual(ApplicationShell.LOGIN_VIEW, "login")
        self.assertEqual(ApplicationShell.APP_VIEW, "app")

    def test_app_shell_navigation_items_include_permission_codes(self) -> None:
        items = {item.key: item for item in AppShell.NAVIGATION_ITEMS}

        self.assertIn("dashboard", items)
        self.assertEqual(
            items["clients"].required_permission,
            PermissionCode.CLIENTS_VIEW.value,
        )
        self.assertEqual(
            items["reports"].required_permission,
            PermissionCode.REPORTS_VIEW.value,
        )


if __name__ == "__main__":
    unittest.main()

