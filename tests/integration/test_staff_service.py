"""
File Purpose: Integration tests for staff account management.
Module: tests.integration.test_staff_service
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
from app.models.staff import StaffInput  # noqa: E402
from app.models.user import CreateUserRequest  # noqa: E402
from app.repositories.user_repository import UserRepository  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402
from app.services.staff_service import StaffService  # noqa: E402


class StaffServiceTest(unittest.TestCase):
    """Tests for staff account management behavior."""

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
        staff_service = StaffService(user_repository)
        return auth_service, user_repository, staff_service

    def test_admin_can_create_search_deactivate_and_activate_staff(self) -> None:
        auth_service, _user_repository, staff_service = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        admin_session = auth_service.authenticate("admin", "StrongPassword123")

        staff_id = staff_service.create_staff(
            admin_session,
            StaffInput(
                full_name="Staff User",
                username="staff",
                password="StrongPassword123",
                mobile="9999999999",
            ),
        )

        staff = staff_service.list_staff(admin_session, "staff")
        self.assertEqual(len(staff), 1)
        self.assertEqual(staff[0].id, staff_id)
        self.assertEqual(staff[0].role_code, RoleCode.STAFF.value)

        staff_service.deactivate_staff(admin_session, staff_id)
        inactive = staff_service.list_staff(admin_session, "staff")
        self.assertFalse(inactive[0].is_active)

        staff_service.activate_staff(admin_session, staff_id)
        active = staff_service.list_staff(admin_session, "staff")
        self.assertTrue(active[0].is_active)

    def test_staff_without_user_manage_cannot_create_staff(self) -> None:
        auth_service, user_repository, staff_service = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        user_repository.create_user(
            CreateUserRequest(
                full_name="Staff User",
                username="staff",
                password_hash=hash_password("StrongPassword123"),
                role_code=RoleCode.STAFF.value,
            )
        )
        staff_session = auth_service.authenticate("staff", "StrongPassword123")

        with self.assertRaises(AuthorizationError):
            staff_service.create_staff(
                staff_session,
                StaffInput("Other Staff", "other", "StrongPassword123"),
            )

    def test_create_staff_validates_duplicate_username(self) -> None:
        auth_service, _user_repository, staff_service = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        admin_session = auth_service.authenticate("admin", "StrongPassword123")
        staff_service.create_staff(
            admin_session,
            StaffInput("Staff User", "staff", "StrongPassword123"),
        )

        with self.assertRaises(ValidationError):
            staff_service.create_staff(
                admin_session,
                StaffInput("Second Staff", "staff", "StrongPassword123"),
            )

    def test_admin_cannot_deactivate_own_account(self) -> None:
        auth_service, _user_repository, staff_service = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        admin_session = auth_service.authenticate("admin", "StrongPassword123")

        with self.assertRaises(ValidationError):
            staff_service.deactivate_staff(admin_session, admin_session.user.id)

    def test_create_staff_validates_password_and_role(self) -> None:
        auth_service, _user_repository, staff_service = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        admin_session = auth_service.authenticate("admin", "StrongPassword123")

        with self.assertRaises(ValidationError):
            staff_service.create_staff(
                admin_session,
                StaffInput("Staff User", "staff", "short"),
            )

        with self.assertRaises(ValidationError):
            staff_service.create_staff(
                admin_session,
                StaffInput("Staff User", "staff", "StrongPassword123", "owner"),
            )


if __name__ == "__main__":
    unittest.main()
