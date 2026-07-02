"""
File Purpose: Integration tests for backup foundation.
Module: tests.integration.test_backup_service
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
from app.models.user import CreateUserRequest  # noqa: E402
from app.repositories.user_repository import UserRepository  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402
from app.services.backup_service import BackupService  # noqa: E402


class BackupServiceTest(unittest.TestCase):
    """Tests for SQLite backup creation and retention."""

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
        backup_service = BackupService(paths)
        return auth_service, user_repository, backup_service

    def test_admin_can_create_and_verify_backup(self) -> None:
        auth_service, _user_repository, backup_service = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        admin_session = auth_service.authenticate("admin", "StrongPassword123")

        result = backup_service.create_backup(admin_session)

        self.assertTrue(result.file_path.exists())
        self.assertGreater(result.size_bytes, 0)
        self.assertTrue(result.integrity_ok)
        self.assertTrue(backup_service.verify_backup(result.file_path))

    def test_list_backups_and_cleanup_old_backups(self) -> None:
        auth_service, _user_repository, backup_service = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        admin_session = auth_service.authenticate("admin", "StrongPassword123")
        backup_service.create_backup(admin_session)
        backup_service.create_backup(admin_session)
        backup_service.create_backup(admin_session)

        self.assertEqual(len(backup_service.list_backups(admin_session)), 3)
        deleted_count = backup_service.cleanup_old_backups(admin_session, keep_latest=2)

        self.assertEqual(deleted_count, 1)
        self.assertEqual(len(backup_service.list_backups(admin_session)), 2)

    def test_staff_without_backup_permission_cannot_create_backup(self) -> None:
        auth_service, user_repository, backup_service = self._build_services()
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
            backup_service.create_backup(staff_session)

    def test_cleanup_requires_positive_retention(self) -> None:
        auth_service, _user_repository, backup_service = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        admin_session = auth_service.authenticate("admin", "StrongPassword123")

        with self.assertRaises(ValidationError):
            backup_service.cleanup_old_backups(admin_session, keep_latest=0)


if __name__ == "__main__":
    unittest.main()
