"""
File Purpose: Integration tests for collection tracking.
Module: tests.integration.test_collection_service
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
from app.models.collection import CollectionInput  # noqa: E402
from app.models.user import CreateUserRequest  # noqa: E402
from app.repositories.billing_repository import BillingRepository  # noqa: E402
from app.repositories.client_repository import ClientRepository  # noqa: E402
from app.repositories.collection_repository import CollectionRepository  # noqa: E402
from app.repositories.user_repository import UserRepository  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402
from app.services.billing_service import BillingService  # noqa: E402
from app.services.client_service import ClientService  # noqa: E402
from app.services.collection_service import CollectionService  # noqa: E402


class CollectionServiceTest(unittest.TestCase):
    """Tests for payment collection behavior."""

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
        collection_service = CollectionService(CollectionRepository(connection_manager))
        return (
            auth_service,
            user_repository,
            client_service,
            billing_service,
            billing_repository,
            collection_service,
        )

    def _create_accountant_bill_context(self):
        (
            auth_service,
            user_repository,
            client_service,
            billing_service,
            billing_repository,
            collection_service,
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
        bill_id = billing_service.create_bill(
            accountant_session,
            BillInput(client_id, "BILL-001", "2026-07-02", "1000.00"),
        )
        return (
            auth_service,
            user_repository,
            accountant_session,
            bill_id,
            billing_service,
            billing_repository,
            collection_service,
        )

    def test_accountant_can_record_partial_and_full_collections(self) -> None:
        (
            _auth_service,
            _user_repository,
            accountant_session,
            bill_id,
            _billing_service,
            billing_repository,
            collection_service,
        ) = self._create_accountant_bill_context()

        first_collection_id = collection_service.record_collection(
            accountant_session,
            CollectionInput(bill_id, "400.00", "2026-07-03", "upi"),
        )
        partial_bill = billing_repository.get_by_id(bill_id)
        self.assertIsNotNone(partial_bill)
        self.assertEqual(partial_bill.status, "partial")

        second_collection_id = collection_service.record_collection(
            accountant_session,
            CollectionInput(bill_id, "600.00", "2026-07-04", "bank"),
        )
        paid_bill = billing_repository.get_by_id(bill_id)
        self.assertIsNotNone(paid_bill)
        self.assertEqual(paid_bill.status, "paid")

        collections = collection_service.list_collections(accountant_session, "BILL-001")
        self.assertEqual({item.id for item in collections}, {first_collection_id, second_collection_id})

    def test_collection_rejects_overpayment_invalid_date_and_payment_mode(self) -> None:
        (
            _auth_service,
            _user_repository,
            accountant_session,
            bill_id,
            _billing_service,
            _billing_repository,
            collection_service,
        ) = self._create_accountant_bill_context()

        with self.assertRaises(ValidationError):
            collection_service.record_collection(
                accountant_session,
                CollectionInput(bill_id, "1000.01", "2026-07-03", "upi"),
            )

        with self.assertRaises(ValidationError):
            collection_service.record_collection(
                accountant_session,
                CollectionInput(bill_id, "100.00", "03-07-2026", "upi"),
            )

        with self.assertRaises(ValidationError):
            collection_service.record_collection(
                accountant_session,
                CollectionInput(bill_id, "100.00", "2026-07-03", "card"),
            )

    def test_collection_rejects_cancelled_bill(self) -> None:
        (
            _auth_service,
            _user_repository,
            accountant_session,
            bill_id,
            billing_service,
            _billing_repository,
            collection_service,
        ) = self._create_accountant_bill_context()
        billing_service.update_status(accountant_session, bill_id, "cancelled")

        with self.assertRaises(ValidationError):
            collection_service.record_collection(
                accountant_session,
                CollectionInput(bill_id, "100.00", "2026-07-03", "cash"),
            )

    def test_staff_without_collection_permission_cannot_record_collection(self) -> None:
        (
            auth_service,
            user_repository,
            _accountant_session,
            bill_id,
            _billing_service,
            _billing_repository,
            collection_service,
        ) = self._create_accountant_bill_context()
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
            collection_service.record_collection(
                staff_session,
                CollectionInput(bill_id, "100.00", "2026-07-03", "cash"),
            )


if __name__ == "__main__":
    unittest.main()
