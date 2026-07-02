"""
File Purpose: Integration tests for reports and CSV exports.
Module: tests.integration.test_report_service
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: csv, pathlib, sys, tempfile, unittest, unittest.mock.
"""

import csv
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
from app.models.billing import BillInput  # noqa: E402
from app.models.client import ClientInput  # noqa: E402
from app.models.collection import CollectionInput  # noqa: E402
from app.models.user import CreateUserRequest  # noqa: E402
from app.models.work import WorkAssignmentInput  # noqa: E402
from app.repositories.billing_repository import BillingRepository  # noqa: E402
from app.repositories.client_repository import ClientRepository  # noqa: E402
from app.repositories.collection_repository import CollectionRepository  # noqa: E402
from app.repositories.report_repository import ReportRepository  # noqa: E402
from app.repositories.user_repository import UserRepository  # noqa: E402
from app.repositories.work_repository import WorkRepository  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402
from app.services.billing_service import BillingService  # noqa: E402
from app.services.client_service import ClientService  # noqa: E402
from app.services.collection_service import CollectionService  # noqa: E402
from app.services.report_service import ReportService  # noqa: E402
from app.services.work_service import WorkService  # noqa: E402


class ReportServiceTest(unittest.TestCase):
    """Tests for report data and CSV exports."""

    def _build_context(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        with patch.dict("os.environ", {"CA_CMS_RUNTIME_ROOT": temp_dir.name}, clear=True):
            config = load_config(project_root=PROJECT_ROOT)
        paths = build_paths(config)
        ensure_runtime_directories(paths)
        connection_manager = create_connection_manager(config, paths)
        initialize_database(connection_manager, paths)
        return paths, connection_manager

    def _seed_report_data(self):
        paths, connection_manager = self._build_context()
        user_repository = UserRepository(connection_manager)
        auth_service = AuthService(user_repository)
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        staff_id = user_repository.create_user(
            CreateUserRequest(
                full_name="Staff",
                username="staff",
                password_hash=hash_password("StrongPassword123"),
                role_code=RoleCode.STAFF.value,
            )
        )
        admin_session = auth_service.authenticate("admin", "StrongPassword123")
        client_service = ClientService(ClientRepository(connection_manager))
        client_id = client_service.create_client(
            admin_session,
            ClientInput(client_name="ABC Traders"),
        )
        work_service = WorkService(WorkRepository(connection_manager))
        work_service.assign_work(
            admin_session,
            WorkAssignmentInput(
                client_id=client_id,
                assigned_to_user_id=staff_id,
                work_type="GST",
                title="GST Filing",
            ),
        )
        billing_service = BillingService(BillingRepository(connection_manager))
        bill_id = billing_service.create_bill(
            admin_session,
            BillInput(client_id, "BILL-001", "2026-07-02", "1000.00"),
        )
        collection_service = CollectionService(CollectionRepository(connection_manager))
        collection_service.record_collection(
            admin_session,
            CollectionInput(bill_id, "250.00", "2026-07-03", "upi"),
        )
        report_service = ReportService(ReportRepository(connection_manager), paths)
        return auth_service, admin_session, report_service

    def test_build_reports_returns_expected_rows(self) -> None:
        _auth_service, admin_session, report_service = self._seed_report_data()

        client_summary = report_service.build_report(admin_session, "client_summary")
        work_summary = report_service.build_report(admin_session, "work_status_summary")
        outstanding = report_service.build_report(admin_session, "outstanding_bills")
        collections = report_service.build_report(admin_session, "collection_summary")

        self.assertEqual(client_summary.rows, (("Active", "1"),))
        self.assertEqual(work_summary.rows, (("Pending", "1"),))
        self.assertEqual(outstanding.rows[0][0], "BILL-001")
        self.assertEqual(outstanding.rows[0][5], "Rs. 750.00")
        self.assertEqual(collections.rows, (("Upi", "1", "Rs. 250.00"),))

    def test_export_csv_writes_report_to_configured_exports_folder(self) -> None:
        _auth_service, admin_session, report_service = self._seed_report_data()

        result = report_service.export_csv(admin_session, "outstanding_bills")

        self.assertTrue(result.file_path.exists())
        self.assertIn("exports", result.file_path.parts)
        with result.file_path.open("r", newline="", encoding="utf-8") as csv_file:
            rows = list(csv.reader(csv_file))
        self.assertEqual(rows[0][0], "Bill No")
        self.assertEqual(rows[1][0], "BILL-001")
        self.assertEqual(result.row_count, 1)

    def test_report_requires_permission_and_valid_report_key(self) -> None:
        auth_service, admin_session, report_service = self._seed_report_data()
        user_repository = auth_service._user_repository
        user_repository.create_user(
            CreateUserRequest(
                full_name="Staff Two",
                username="staff2",
                password_hash=hash_password("StrongPassword123"),
                role_code=RoleCode.STAFF.value,
            )
        )
        staff_session = auth_service.authenticate("staff2", "StrongPassword123")

        with self.assertRaises(AuthorizationError):
            report_service.build_report(staff_session, "client_summary")
        with self.assertRaises(ValidationError):
            report_service.build_report(admin_session, "missing_report")


if __name__ == "__main__":
    unittest.main()
