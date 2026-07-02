"""
File Purpose: Integration tests for work assignment and status workflows.
Module: tests.integration.test_work_service
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
from app.models.work import WorkAssignmentInput  # noqa: E402
from app.repositories.client_repository import ClientRepository  # noqa: E402
from app.repositories.user_repository import UserRepository  # noqa: E402
from app.repositories.work_repository import WorkRepository  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402
from app.services.client_service import ClientService  # noqa: E402
from app.services.work_service import WorkService  # noqa: E402


class WorkServiceTest(unittest.TestCase):
    """Tests for work assignment, visibility, and status behavior."""

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
        work_repository = WorkRepository(connection_manager)
        work_service = WorkService(work_repository)
        return auth_service, user_repository, client_service, work_service, work_repository

    def _create_admin_staff_and_client(self):
        (
            auth_service,
            user_repository,
            client_service,
            work_service,
            work_repository,
        ) = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        staff_id = user_repository.create_user(
            CreateUserRequest(
                full_name="Staff User",
                username="staff",
                password_hash=hash_password("StrongPassword123"),
                role_code=RoleCode.STAFF.value,
            )
        )
        admin_session = auth_service.authenticate("admin", "StrongPassword123")
        staff_session = auth_service.authenticate("staff", "StrongPassword123")
        client_id = client_service.create_client(
            admin_session,
            ClientInput(client_name="ABC Traders", mobile="9999999999"),
        )
        return (
            auth_service,
            user_repository,
            admin_session,
            staff_session,
            staff_id,
            client_id,
            work_service,
            work_repository,
        )

    def test_admin_can_assign_work_and_staff_can_view_assigned_work(self) -> None:
        (
            _auth_service,
            _user_repository,
            admin_session,
            staff_session,
            staff_id,
            client_id,
            work_service,
            _work_repository,
        ) = self._create_admin_staff_and_client()

        work_id = work_service.assign_work(
            admin_session,
            WorkAssignmentInput(
                client_id=client_id,
                assigned_to_user_id=staff_id,
                work_type="GST",
                title="July GST Return",
                due_date="2026-07-20",
            ),
        )

        staff_work = work_service.list_work(staff_session)
        self.assertEqual(len(staff_work), 1)
        self.assertEqual(staff_work[0].id, work_id)
        self.assertEqual(staff_work[0].title, "July GST Return")

    def test_staff_cannot_view_other_staff_work(self) -> None:
        (
            auth_service,
            user_repository,
            admin_session,
            staff_session,
            _staff_id,
            client_id,
            work_service,
            _work_repository,
        ) = self._create_admin_staff_and_client()
        other_staff_id = user_repository.create_user(
            CreateUserRequest(
                full_name="Other Staff",
                username="otherstaff",
                password_hash=hash_password("StrongPassword123"),
                role_code=RoleCode.STAFF.value,
            )
        )
        auth_service.authenticate("otherstaff", "StrongPassword123")

        work_service.assign_work(
            admin_session,
            WorkAssignmentInput(
                client_id=client_id,
                assigned_to_user_id=other_staff_id,
                work_type="Income Tax",
                title="ITR Preparation",
            ),
        )

        self.assertEqual(work_service.list_work(staff_session), [])

    def test_staff_can_update_assigned_status_and_add_remark(self) -> None:
        (
            _auth_service,
            _user_repository,
            admin_session,
            staff_session,
            staff_id,
            client_id,
            work_service,
            work_repository,
        ) = self._create_admin_staff_and_client()
        work_id = work_service.assign_work(
            admin_session,
            WorkAssignmentInput(
                client_id=client_id,
                assigned_to_user_id=staff_id,
                work_type="GST",
                title="GSTR-1 Filing",
            ),
        )

        work_service.update_status(
            staff_session,
            work_id,
            "completed",
            "Filed and shared acknowledgement.",
        )

        updated = work_repository.get_by_id(work_id)
        self.assertIsNotNone(updated)
        self.assertEqual(updated.status, "completed")
        self.assertIsNotNone(updated.completed_at)
        self.assertEqual(work_repository.count_remarks(work_id), 1)

    def test_staff_cannot_update_unassigned_work(self) -> None:
        (
            _auth_service,
            user_repository,
            admin_session,
            staff_session,
            _staff_id,
            client_id,
            work_service,
            _work_repository,
        ) = self._create_admin_staff_and_client()
        other_staff_id = user_repository.create_user(
            CreateUserRequest(
                full_name="Other Staff",
                username="otherstaff",
                password_hash=hash_password("StrongPassword123"),
                role_code=RoleCode.STAFF.value,
            )
        )
        work_id = work_service.assign_work(
            admin_session,
            WorkAssignmentInput(
                client_id=client_id,
                assigned_to_user_id=other_staff_id,
                work_type="Audit",
                title="Stock Audit",
            ),
        )

        with self.assertRaises(AuthorizationError):
            work_service.update_status(staff_session, work_id, "in_progress")

    def test_assign_work_validates_due_date(self) -> None:
        (
            _auth_service,
            _user_repository,
            admin_session,
            _staff_session,
            staff_id,
            client_id,
            work_service,
            _work_repository,
        ) = self._create_admin_staff_and_client()

        with self.assertRaises(ValidationError):
            work_service.assign_work(
                admin_session,
                WorkAssignmentInput(
                    client_id=client_id,
                    assigned_to_user_id=staff_id,
                    work_type="GST",
                    title="Invalid Due Date",
                    due_date="20-07-2026",
                ),
            )


if __name__ == "__main__":
    unittest.main()
