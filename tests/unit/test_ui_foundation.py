"""
File Purpose: Unit tests for UI foundation imports and theme tokens.
Module: tests.unit.test_ui_foundation
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

from app.ui import (  # noqa: E402
    DataTable,
    FormField,
    NavigationItem,
    PrimaryButton,
    ThemeManager,
    WindowManager,
    theme_manager,
)


class UIFoundationTest(unittest.TestCase):
    """Tests that UI foundation modules are importable without launching screens."""

    def test_theme_tokens_are_available(self) -> None:
        self.assertIsInstance(theme_manager, ThemeManager)
        self.assertEqual(theme_manager.color("primary"), ("#1F6F78", "#3AA6B2"))
        self.assertEqual(theme_manager.tokens.spacing.sm, 8)

    def test_component_classes_are_exported(self) -> None:
        self.assertIsNotNone(PrimaryButton)
        self.assertIsNotNone(FormField)
        self.assertIsNotNone(DataTable)
        self.assertIsNotNone(WindowManager)

    def test_navigation_item_model(self) -> None:
        item = NavigationItem(
            key="clients",
            label="Clients",
            required_permission="clients.view",
        )

        self.assertEqual(item.key, "clients")
        self.assertEqual(item.required_permission, "clients.view")


if __name__ == "__main__":
    unittest.main()

