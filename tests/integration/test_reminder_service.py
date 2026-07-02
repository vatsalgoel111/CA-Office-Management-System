"""
File Purpose: Integration tests for reminder system foundation.
Module: tests.integration.test_reminder_service
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: datetime, pathlib, sys, tempfile, unittest, unittest.mock.
"""

from datetime import date, timedelta
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
from app.models.work import WorkAssignmentInput  # noqa: E402
from app.repositories.client_repository import ClientRepository  # noqa: E402
from app.repositories.reminder_repository import ReminderRepository  # noqa: E402
from app.repositories.user_repository import UserRepository  # noqa: E402
from app.repositories.work_repository import WorkRepository  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402
from app.services.client_service import ClientService  # noqa: E402
from app.services.reminder_service import ReminderService  # noqa: E402
from app.services.work_service import WorkService  # noqa: E402


class ReminderServiceTest(unittest.TestCase):
    """Tests for overdue and upcoming work reminders."""

    def _build_context(self):
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
        reminder_service = ReminderService(ReminderRepository(connection_manager))
        return connection_manager, auth_service, user_repository, reminder_service

    def _seed_work(self):
        connection_manager, auth_service, user_repository, reminder_service = self._build_context()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        staff_id = user_repository.create_user(
            CreateUserRequest(
                full_name="Staff",
                username="staff",
                password_hash=hash_password("StrongPassword123"),
                role_code=RoleCode.STAFF.value,
            )
        )
        other_staff_id = user_repository.create_user(
            CreateUserRequest(
                full_name="Other Staff",
                username="other",
                password_hash=hash_password("StrongPassword123"),
                role_code=RoleCode.STAFF.value,
            )
        )
        admin_session = auth_service.authenticate("admin", "StrongPassword123")
        staff_session = auth_service.authenticate("staff", "StrongPassword123")
        client_id = ClientService(ClientRepository(connection_manager)).create_client(
            admin_session,
            ClientInput("ABC Traders"),
        )
        work_service = WorkService(WorkRepository(connection_manager))
        today = date(2026, 7, 2)
        work_service.assign_work(
            admin_session,
            WorkAssignmentInput(
                client_id,
                staff_id,
                "GST",
                "Overdue GST",
                due_date=(today - timedelta(days=2)).isoformat(),
            ),
        )
        work_service.assign_work(
            admin_session,
            WorkAssignmentInput(
                client_id,
                staff_id,
                "ITR",
                "Upcoming ITR",
                due_date=(today + timedelta(days=3)).isoformat(),
            ),
        )
        work_service.assign_work(
            admin_session,
            WorkAssignmentInput(
                client_id,
                other_staff_id,
                "Audit",
                "Other Staff Audit",
                due_date=(today + timedelta(days=1)).isoformat(),
            ),
        )
        return auth_service, admin_session, staff_session, reminder_service, today

    def test_admin_sees_all_overdue_and_upcoming_work(self) -> None:
        _auth_service, admin_session, _staff_session, reminder_service, today = self._seed_work()

        summary = reminder_service.get_summary(admin_session, today=today)

        self.assertEqual(summary.overdue_count, 1)
        self.assertEqual(summary.upcoming_count, 2)
        self.assertEqual(len(summary.reminders), 3)

    def test_staff_sees_assigned_reminders_only(self) -> None:
        _auth_service, _admin_session, staff_session, reminder_service, today = self._seed_work()

        summary = reminder_service.get_summary(staff_session, today=today)

        self.assertEqual(summary.overdue_count, 1)
        self.assertEqual(summary.upcoming_count, 1)
        self.assertEqual({item.title for item in summary.reminders}, {"Overdue GST", "Upcoming ITR"})

    def test_reminder_validates_range_and_permissions(self) -> None:
        auth_service, _admin_session, _staff_session, reminder_service, today = self._seed_work()
        user_repository = auth_service._user_repository
        user_repository.create_user(
            CreateUserRequest(
                full_name="Accountant",
                username="accountant",
                password_hash=hash_password("StrongPassword123"),
                role_code=RoleCode.ACCOUNTANT.value,
            )
        )
        accountant_session = auth_service.authenticate("accountant", "StrongPassword123")

        with self.assertRaises(ValidationError):
            reminder_service.get_summary(accountant_session, today=today, upcoming_days=91)
        with self.assertRaises(AuthorizationError):
            reminder_service.get_summary(accountant_session, today=today)


if __name__ == "__main__":
    unittest.main()
