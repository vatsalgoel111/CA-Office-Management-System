"""
File Purpose: Integration tests for dashboard summary behavior.
Module: tests.integration.test_dashboard_service
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
from app.core.paths import build_paths, ensure_runtime_directories  # noqa: E402
from app.core.security import hash_password  # noqa: E402
from app.database.connection import create_connection_manager  # noqa: E402
from app.database.initializer import initialize_database  # noqa: E402
from app.models.user import CreateUserRequest  # noqa: E402
from app.repositories.dashboard_repository import DashboardRepository  # noqa: E402
from app.repositories.user_repository import UserRepository  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402
from app.services.dashboard_service import DashboardService  # noqa: E402


class DashboardServiceTest(unittest.TestCase):
    """Tests for dashboard summaries backed by SQLite."""

    def _build_context(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        with patch.dict("os.environ", {"CA_CMS_RUNTIME_ROOT": temp_dir.name}, clear=True):
            config = load_config(project_root=PROJECT_ROOT)
        paths = build_paths(config)
        ensure_runtime_directories(paths)
        connection_manager = create_connection_manager(config, paths)
        initialize_database(connection_manager, paths)
        return connection_manager

    def test_admin_summary_counts_all_work(self) -> None:
        connection_manager = self._build_context()
        user_repository = UserRepository(connection_manager)
        auth_service = AuthService(user_repository)
        admin_id = auth_service.create_initial_admin(
            full_name="Admin",
            username="admin",
            password="StrongPassword123",
        )
        staff_id = user_repository.create_user(
            CreateUserRequest(
                full_name="Staff",
                username="staff",
                password_hash=hash_password("StrongPassword123"),
                role_code=RoleCode.STAFF.value,
            )
        )
        self._seed_dashboard_data(connection_manager, admin_id, staff_id)

        session = auth_service.authenticate("admin", "StrongPassword123")
        summary = DashboardService(
            DashboardRepository(connection_manager)
        ).get_summary(session, today=date.today())

        self.assertEqual(summary.active_clients, 1)
        self.assertEqual(summary.pending_work, 2)
        self.assertEqual(summary.overdue_work, 1)
        self.assertEqual(summary.completed_work, 1)
        self.assertEqual(summary.unpaid_bills, 2)
        self.assertEqual(summary.outstanding_amount_paise, 125000)

    def test_staff_summary_counts_assigned_work_only(self) -> None:
        connection_manager = self._build_context()
        user_repository = UserRepository(connection_manager)
        auth_service = AuthService(user_repository)
        admin_id = auth_service.create_initial_admin(
            full_name="Admin",
            username="admin",
            password="StrongPassword123",
        )
        staff_id = user_repository.create_user(
            CreateUserRequest(
                full_name="Staff",
                username="staff",
                password_hash=hash_password("StrongPassword123"),
                role_code=RoleCode.STAFF.value,
            )
        )
        self._seed_dashboard_data(connection_manager, admin_id, staff_id)

        session = auth_service.authenticate("staff", "StrongPassword123")
        summary = DashboardService(
            DashboardRepository(connection_manager)
        ).get_summary(session, today=date.today())

        self.assertEqual(summary.pending_work, 1)
        self.assertEqual(summary.overdue_work, 1)
        self.assertEqual(summary.completed_work, 0)

    def _seed_dashboard_data(self, connection_manager, admin_id: int, staff_id: int) -> None:
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        tomorrow = (date.today() + timedelta(days=1)).isoformat()

        with connection_manager.transaction() as connection:
            cursor = connection.execute(
                """
                INSERT INTO clients (client_name, status)
                VALUES ('ABC Traders', 'active');
                """
            )
            client_id = int(cursor.lastrowid)
            connection.execute(
                """
                INSERT INTO work_items (
                    client_id,
                    assigned_to_user_id,
                    assigned_by_user_id,
                    work_type,
                    title,
                    status,
                    due_date
                )
                VALUES (?, ?, ?, 'GST', 'Overdue GST', 'pending', ?);
                """,
                (client_id, staff_id, admin_id, yesterday),
            )
            connection.execute(
                """
                INSERT INTO work_items (
                    client_id,
                    assigned_to_user_id,
                    assigned_by_user_id,
                    work_type,
                    title,
                    status,
                    due_date
                )
                VALUES (?, ?, ?, 'ITR', 'Upcoming ITR', 'in_progress', ?);
                """,
                (client_id, admin_id, admin_id, tomorrow),
            )
            connection.execute(
                """
                INSERT INTO work_items (
                    client_id,
                    assigned_to_user_id,
                    assigned_by_user_id,
                    work_type,
                    title,
                    status,
                    completed_at
                )
                VALUES (?, ?, ?, 'Audit', 'Completed Audit', 'completed', ?);
                """,
                (client_id, admin_id, admin_id, date.today().isoformat()),
            )
            bill_cursor = connection.execute(
                """
                INSERT INTO bills (client_id, bill_number, bill_date, amount_paise, status)
                VALUES (?, 'BILL-001', ?, 100000, 'partial');
                """,
                (client_id, date.today().isoformat()),
            )
            partial_bill_id = int(bill_cursor.lastrowid)
            connection.execute(
                """
                INSERT INTO collections (bill_id, received_amount_paise, received_date)
                VALUES (?, 25000, ?);
                """,
                (partial_bill_id, date.today().isoformat()),
            )
            connection.execute(
                """
                INSERT INTO bills (client_id, bill_number, bill_date, amount_paise, status)
                VALUES (?, 'BILL-002', ?, 50000, 'unpaid');
                """,
                (client_id, date.today().isoformat()),
            )


if __name__ == "__main__":
    unittest.main()

