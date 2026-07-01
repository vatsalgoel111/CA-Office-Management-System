"""
File Purpose: Integration tests for authentication service and RBAC.
Module: tests.integration.test_auth_service
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
from app.constants import PermissionCode  # noqa: E402
from app.core.exceptions import AuthenticationError, AuthorizationError  # noqa: E402
from app.core.paths import build_paths, ensure_runtime_directories  # noqa: E402
from app.database.connection import create_connection_manager  # noqa: E402
from app.database.initializer import initialize_database  # noqa: E402
from app.repositories.user_repository import UserRepository  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402


class AuthServiceTest(unittest.TestCase):
    """Tests for authentication against initialized SQLite database."""

    def _build_service(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        env = {"CA_CMS_RUNTIME_ROOT": temp_dir.name}
        with patch.dict("os.environ", env, clear=True):
            config = load_config(project_root=PROJECT_ROOT)
        paths = build_paths(config)
        ensure_runtime_directories(paths)
        connection_manager = create_connection_manager(config, paths)
        initialize_database(connection_manager, paths)
        repository = UserRepository(connection_manager)
        return AuthService(repository), repository

    def test_create_initial_admin_and_authenticate(self) -> None:
        auth_service, _repository = self._build_service()
        auth_service.create_initial_admin(
            full_name="Admin User",
            username="Admin",
            password="StrongPassword123",
        )

        session = auth_service.authenticate("admin", "StrongPassword123")

        self.assertEqual(session.user.username, "admin")
        self.assertTrue(session.has_permission(PermissionCode.USERS_MANAGE.value))

    def test_authenticate_rejects_wrong_password(self) -> None:
        auth_service, _repository = self._build_service()
        auth_service.create_initial_admin(
            full_name="Admin User",
            username="admin",
            password="StrongPassword123",
        )

        with self.assertRaises(AuthenticationError):
            auth_service.authenticate("admin", "bad-password")

    def test_initial_admin_can_only_be_created_once(self) -> None:
        auth_service, _repository = self._build_service()
        auth_service.create_initial_admin(
            full_name="Admin User",
            username="admin",
            password="StrongPassword123",
        )

        with self.assertRaises(AuthenticationError):
            auth_service.create_initial_admin(
                full_name="Second Admin",
                username="admin2",
                password="StrongPassword123",
            )

    def test_require_permission_rejects_missing_permission(self) -> None:
        auth_service, _repository = self._build_service()
        auth_service.create_initial_admin(
            full_name="Admin User",
            username="admin",
            password="StrongPassword123",
        )
        session = auth_service.authenticate("admin", "StrongPassword123")

        with self.assertRaises(AuthorizationError):
            auth_service.require_permission(session, "not.real")


if __name__ == "__main__":
    unittest.main()

