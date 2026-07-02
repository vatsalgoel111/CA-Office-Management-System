"""
File Purpose: Integration tests for billing management.
Module: tests.integration.test_billing_service
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
from app.models.billing import BillInput  # noqa: E402
from app.models.client import ClientInput  # noqa: E402
from app.models.user import CreateUserRequest  # noqa: E402
from app.repositories.billing_repository import BillingRepository  # noqa: E402
from app.repositories.client_repository import ClientRepository  # noqa: E402
from app.repositories.user_repository import UserRepository  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402
from app.services.billing_service import BillingService  # noqa: E402
from app.services.client_service import ClientService  # noqa: E402


class BillingServiceTest(unittest.TestCase):
    """Tests for bill creation, listing, and status updates."""

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
        billing_repository = BillingRepository(connection_manager)
        billing_service = BillingService(billing_repository)
        return auth_service, user_repository, client_service, billing_service, billing_repository

    def _create_admin_accountant_and_client(self):
        (
            auth_service,
            user_repository,
            client_service,
            billing_service,
            billing_repository,
        ) = self._build_services()
        auth_service.create_initial_admin("Admin", "admin", "StrongPassword123")
        user_repository.create_user(
            CreateUserRequest(
                full_name="Accountant",
                username="accountant",
                password_hash=hash_password("StrongPassword123"),
                role_code=RoleCode.ACCOUNTANT.value,
            )
        )
        admin_session = auth_service.authenticate("admin", "StrongPassword123")
        accountant_session = auth_service.authenticate(
            "accountant",
            "StrongPassword123",
        )
        client_id = client_service.create_client(
            admin_session,
            ClientInput(client_name="ABC Traders"),
        )
        return (
            auth_service,
            user_repository,
            accountant_session,
            client_id,
            billing_service,
            billing_repository,
        )

    def test_accountant_can_create_list_and_mark_bill_paid(self) -> None:
        (
            _auth_service,
            _user_repository,
            accountant_session,
            client_id,
            billing_service,
            billing_repository,
        ) = self._create_admin_accountant_and_client()

        bill_id = billing_service.create_bill(
            accountant_session,
            BillInput(
                client_id=client_id,
                bill_number="BILL-001",
                bill_date="2026-07-02",
                amount_rupees="1250.50",
            ),
        )

        bills = billing_service.list_bills(accountant_session, "BILL-001")
        self.assertEqual(len(bills), 1)
        self.assertEqual(bills[0].id, bill_id)
        self.assertEqual(bills[0].amount_paise, 125050)
        self.assertEqual(bills[0].status, "unpaid")

        billing_service.update_status(accountant_session, bill_id, "paid")
        updated = billing_repository.get_by_id(bill_id)
        self.assertIsNotNone(updated)
        self.assertEqual(updated.status, "paid")

    def test_staff_without_billing_permission_cannot_list_bills(self) -> None:
        (
            auth_service,
            user_repository,
            _accountant_session,
            _client_id,
            billing_service,
            _billing_repository,
        ) = self._create_admin_accountant_and_client()
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
            billing_service.list_bills(staff_session)

    def test_create_bill_validates_amount_date_and_duplicate_number(self) -> None:
        (
            _auth_service,
            _user_repository,
            accountant_session,
            client_id,
            billing_service,
            _billing_repository,
        ) = self._create_admin_accountant_and_client()

        with self.assertRaises(ValidationError):
            billing_service.create_bill(
                accountant_session,
                BillInput(client_id, "BILL-001", "2026-07-02", "0"),
            )

        with self.assertRaises(ValidationError):
            billing_service.create_bill(
                accountant_session,
                BillInput(client_id, "BILL-001", "02-07-2026", "100"),
            )

        billing_service.create_bill(
            accountant_session,
            BillInput(client_id, "BILL-001", "2026-07-02", "100"),
        )
        with self.assertRaises(ValidationError):
            billing_service.create_bill(
                accountant_session,
                BillInput(client_id, "BILL-001", "2026-07-03", "200"),
            )

    def test_create_bill_rejects_missing_client_and_work_item(self) -> None:
        (
            _auth_service,
            _user_repository,
            accountant_session,
            client_id,
            billing_service,
            _billing_repository,
        ) = self._create_admin_accountant_and_client()

        with self.assertRaises(ValidationError):
            billing_service.create_bill(
                accountant_session,
                BillInput(999, "BILL-001", "2026-07-02", "100"),
            )

        with self.assertRaises(ValidationError):
            billing_service.create_bill(
                accountant_session,
                BillInput(client_id, "BILL-001", "2026-07-02", "100", 999),
            )


if __name__ == "__main__":
    unittest.main()
