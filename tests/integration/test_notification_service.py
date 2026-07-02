"""
File Purpose: Integration tests for notification and WhatsApp foundation.
Module: tests.integration.test_notification_service
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
from app.models.notification import NotificationInput  # noqa: E402
from app.models.user import CreateUserRequest  # noqa: E402
from app.repositories.notification_repository import NotificationRepository  # noqa: E402
from app.repositories.user_repository import UserRepository  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402
from app.services.notification_service import NotificationService  # noqa: E402


class NotificationServiceTest(unittest.TestCase):
    """Tests for provider-neutral notification queue behavior."""

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
        notification_service = NotificationService(
            NotificationRepository(connection_manager)
        )
        return auth_service, user_repository, notification_service

    def test_admin_can_queue_whatsapp_notification_and_mark_sent(self) -> None:
        auth_service, user_repository, notification_service = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        recipient_id = user_repository.create_user(
            CreateUserRequest(
                full_name="Staff",
                username="staff",
                password_hash=hash_password("StrongPassword123"),
                role_code=RoleCode.STAFF.value,
            )
        )
        admin_session = auth_service.authenticate("admin", "StrongPassword123")

        notification_id = notification_service.queue_whatsapp_message(
            admin_session,
            recipient_id,
            "New work assigned.",
            "work_assigned",
        )
        notification_service.mark_sent(admin_session, notification_id)

        notifications = notification_service.list_notifications(admin_session)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].provider, "whatsapp")
        self.assertEqual(notifications[0].status, "sent")

    def test_staff_without_settings_permission_cannot_queue_notification(self) -> None:
        auth_service, user_repository, notification_service = self._build_services()
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
            notification_service.queue_notification(
                staff_session,
                NotificationInput(1, "manual", "Hello"),
            )

    def test_notification_validates_recipient_type_provider_and_message(self) -> None:
        auth_service, _user_repository, notification_service = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        admin_session = auth_service.authenticate("admin", "StrongPassword123")

        with self.assertRaises(ValidationError):
            notification_service.queue_notification(
                admin_session,
                NotificationInput(999, "manual", "Hello"),
            )
        with self.assertRaises(ValidationError):
            notification_service.queue_notification(
                admin_session,
                NotificationInput(admin_session.user.id, "unknown", "Hello"),
            )
        with self.assertRaises(ValidationError):
            notification_service.queue_notification(
                admin_session,
                NotificationInput(admin_session.user.id, "manual", "Hello", "sms"),
            )
        with self.assertRaises(ValidationError):
            notification_service.queue_notification(
                admin_session,
                NotificationInput(admin_session.user.id, "manual", " "),
            )


if __name__ == "__main__":
    unittest.main()
