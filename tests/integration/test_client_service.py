"""
File Purpose: Integration tests for client management service and repository.
Module: tests.integration.test_client_service
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
from app.models.client import ClientInput  # noqa: E402
from app.models.user import CreateUserRequest  # noqa: E402
from app.repositories.client_repository import ClientRepository  # noqa: E402
from app.repositories.user_repository import UserRepository  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402
from app.services.client_service import ClientService  # noqa: E402


class ClientServiceTest(unittest.TestCase):
    """Tests for client management behavior."""

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
        client_service = ClientService(ClientRepository(connection_manager))
        return auth_service, user_repository, client_service

    def test_admin_can_create_search_update_and_deactivate_client(self) -> None:
        auth_service, _user_repository, client_service = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        session = auth_service.authenticate("admin", "StrongPassword123")

        client_id = client_service.create_client(
            session,
            ClientInput(
                client_name="ABC Traders",
                business_name="ABC Trading Co",
                mobile="9999999999",
                pan="abcde1234f",
            ),
        )
        clients = client_service.search_clients(session, "ABC")
        self.assertEqual(len(clients), 1)
        self.assertEqual(clients[0].id, client_id)
        self.assertEqual(clients[0].pan, "ABCDE1234F")

        client_service.update_client(
            session,
            client_id,
            ClientInput(client_name="ABC Traders Updated", email="abc@example.com"),
        )
        updated = client_service.search_clients(session, "Updated")
        self.assertEqual(updated[0].email, "abc@example.com")

        client_service.deactivate_client(session, client_id)
        self.assertEqual(client_service.search_clients(session, "ABC"), [])
        inactive = client_service.search_clients(session, "ABC", include_inactive=True)
        self.assertEqual(inactive[0].status, "inactive")

    def test_create_client_requires_name(self) -> None:
        auth_service, _user_repository, client_service = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        session = auth_service.authenticate("admin", "StrongPassword123")

        with self.assertRaises(ValidationError):
            client_service.create_client(session, ClientInput(client_name=" "))

    def test_staff_cannot_create_client_without_permission(self) -> None:
        auth_service, user_repository, client_service = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        user_repository.create_user(
            CreateUserRequest(
                full_name="Staff",
                username="staff",
                password_hash=hash_password("StrongPassword123"),
                role_code=RoleCode.STAFF.value,
            )
        )
        session = auth_service.authenticate("staff", "StrongPassword123")

        with self.assertRaises(AuthorizationError):
            client_service.create_client(session, ClientInput(client_name="ABC Traders"))


if __name__ == "__main__":
    unittest.main()

