"""
File Purpose: Integration tests for audit log foundation.
Module: tests.integration.test_audit_service
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
from app.repositories.audit_repository import AuditRepository  # noqa: E402
from app.repositories.user_repository import UserRepository  # noqa: E402
from app.services.audit_service import AuditService  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402


class AuditServiceTest(unittest.TestCase):
    """Tests for audit recording and viewing."""

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
        audit_service = AuditService(AuditRepository(connection_manager))
        return auth_service, user_repository, audit_service

    def test_admin_can_record_and_view_audit_event(self) -> None:
        auth_service, _user_repository, audit_service = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        admin_session = auth_service.authenticate("admin", "StrongPassword123")

        audit_id = audit_service.record_event(
            admin_session,
            action="create",
            entity_type="client",
            entity_id=10,
            old_values=None,
            new_values={"client_name": "ABC Traders"},
            description="Created client ABC Traders",
        )

        entries = audit_service.list_entries(admin_session, "abc")
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].id, audit_id)
        self.assertEqual(entries[0].username, "admin")
        self.assertEqual(entries[0].action, "create")
        self.assertIn("ABC Traders", entries[0].new_values)

    def test_system_event_can_be_recorded_without_session(self) -> None:
        auth_service, _user_repository, audit_service = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        admin_session = auth_service.authenticate("admin", "StrongPassword123")

        audit_service.record_event(
            None,
            action="backup",
            entity_type="system",
            description="Automatic backup completed",
        )

        entries = audit_service.list_entries(admin_session, "backup")
        self.assertEqual(entries[0].username, None)
        self.assertEqual(entries[0].description, "Automatic backup completed")

    def test_staff_without_audit_permission_cannot_view_entries(self) -> None:
        auth_service, user_repository, audit_service = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        admin_session = auth_service.authenticate("admin", "StrongPassword123")
        user_repository.create_user(
            CreateUserRequest(
                full_name="Staff",
                username="staff",
                password_hash=hash_password("StrongPassword123"),
                role_code=RoleCode.STAFF.value,
            )
        )
        staff_session = auth_service.authenticate("staff", "StrongPassword123")
        audit_service.record_event(admin_session, "create", "client", "Created client")

        with self.assertRaises(AuthorizationError):
            audit_service.list_entries(staff_session)

    def test_audit_validates_required_fields_and_limit(self) -> None:
        auth_service, _user_repository, audit_service = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        admin_session = auth_service.authenticate("admin", "StrongPassword123")

        with self.assertRaises(ValidationError):
            audit_service.record_event(admin_session, " ", "client", "Created client")
        with self.assertRaises(ValidationError):
            audit_service.list_entries(admin_session, limit=0)


if __name__ == "__main__":
    unittest.main()
