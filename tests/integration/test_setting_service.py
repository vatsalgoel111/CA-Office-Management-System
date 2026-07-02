"""
File Purpose: Integration tests for settings foundation.
Module: tests.integration.test_setting_service
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: pathlib, sys, tempfile, unittest, unittest.mock.
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
from app.constants import RoleCode  # noqa: E402
from app.core.exceptions import AuthorizationError, ValidationError  # noqa: E402
from app.core.paths import build_paths, ensure_runtime_directories  # noqa: E402
from app.core.security import hash_password  # noqa: E402
from app.database.connection import create_connection_manager  # noqa: E402
from app.database.initializer import initialize_database  # noqa: E402
from app.models.setting import SettingInput  # noqa: E402
from app.models.user import CreateUserRequest  # noqa: E402
from app.repositories.setting_repository import SettingRepository  # noqa: E402
from app.repositories.user_repository import UserRepository  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402
from app.services.setting_service import SettingService  # noqa: E402


class SettingServiceTest(unittest.TestCase):
    """Tests for application setting management."""

    def _build_services(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        with patch.dict("os.environ", {"CA_CMS_RUNTIME_ROOT": temp_dir.name}, clear=True):
            config = load_config(project_root=PROJECT_ROOT)
        paths = build_paths(config)
        ensure_runtime_directories(paths)
        connection_manager = create_connection_manager(config, paths)
        initialize_database(connection_manager, paths)
        user_repository = UserRepository(connection_manager)
        auth_service = AuthService(user_repository)
        setting_service = SettingService(SettingRepository(connection_manager))
        return auth_service, user_repository, setting_service

    def test_admin_can_list_and_update_settings(self) -> None:
        auth_service, _user_repository, setting_service = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        admin_session = auth_service.authenticate("admin", "StrongPassword123")

        settings = setting_service.list_settings(admin_session)
        self.assertGreaterEqual(len(settings), 4)

        setting_service.update_setting(
            admin_session,
            SettingInput("app.theme", "light"),
        )
        self.assertEqual(setting_service.get_value("app.theme"), "light")

    def test_staff_without_settings_permission_cannot_update_settings(self) -> None:
        auth_service, user_repository, setting_service = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        user_repository.create_user(
            CreateUserRequest(
                full_name="Staff",
                username="staff",
                password_hash=hash_password("StrongPassword123"),
                role_code=RoleCode.STAFF.value,
            )
        )
        staff_session = auth_service.authenticate("staff", "StrongPassword123")

        with self.assertRaises(AuthorizationError):
            setting_service.update_setting(
                staff_session,
                SettingInput("app.theme", "dark"),
            )

    def test_setting_validation_for_boolean_and_enum_values(self) -> None:
        auth_service, _user_repository, setting_service = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        admin_session = auth_service.authenticate("admin", "StrongPassword123")

        with self.assertRaises(ValidationError):
            setting_service.update_setting(
                admin_session,
                SettingInput("backup.auto_enabled", "sometimes"),
            )
        with self.assertRaises(ValidationError):
            setting_service.update_setting(
                admin_session,
                SettingInput("backup.frequency", "hourly"),
            )
        with self.assertRaises(ValidationError):
            setting_service.update_setting(admin_session, SettingInput(" ", "value"))


if __name__ == "__main__":
    unittest.main()
