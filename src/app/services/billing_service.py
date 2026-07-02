"""
File Purpose: Billing business logic and permission checks.
Module: app.services.billing_service
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: datetime, decimal, typing, app.constants, app.core.exceptions, app.models, app.repositories.
"""

from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import List

from app.constants import PermissionCode
from app.core.exceptions import AuthorizationError, ValidationError
from app.models.billing import Bill, BillInput
from app.models.session import UserSession
from app.repositories.billing_repository import BillingRepository


VALID_BILL_STATUSES = {"unpaid", "partial", "paid", "cancelled"}


class BillingService:
    """Business logic for bill management."""

    def __init__(self, billing_repository: BillingRepository) -> None:
        self._billing_repository = billing_repository

    def list_bills(self, session: UserSession, search_text: str = "") -> List[Bill]:
        """List bills after permission check."""

        self._require(session)
        return self._billing_repository.list_bills(search_text)

    def create_bill(self, session: UserSession, bill_input: BillInput) -> int:
        """Create a bill after validation."""

        self._require(session)
        amount_paise = self._validate_bill_input(bill_input)
        return self._billing_repository.create(bill_input, amount_paise)

    def update_status(self, session: UserSession, bill_id: int, status: str) -> None:
        """Update bill status."""

        self._require(session)
        normalized_status = status.strip().lower()
        if normalized_status not in VALID_BILL_STATUSES:
            raise ValidationError("Invalid bill status")
        if self._billing_repository.get_by_id(bill_id) is None:
            raise ValidationError("Bill not found")
        self._billing_repository.update_status(bill_id, normalized_status)

    def _validate_bill_input(self, bill_input: BillInput) -> int:
        if bill_input.client_id <= 0:
            raise ValidationError("Client is required")
        if not self._billing_repository.client_exists(bill_input.client_id):
            raise ValidationError("Active client not found")
        if bill_input.work_item_id is not None and bill_input.work_item_id <= 0:
            raise ValidationError("Work item ID is invalid")
        if (
            bill_input.work_item_id is not None
            and not self._billing_repository.work_item_exists(bill_input.work_item_id)
        ):
            raise ValidationError("Work item not found")
        if not bill_input.bill_number.strip():
            raise ValidationError("Bill number is required")
        if self._billing_repository.bill_number_exists(bill_input.bill_number):
            raise ValidationError("Bill number already exists")
        try:
            date.fromisoformat(bill_input.bill_date)
        except ValueError as exc:
            raise ValidationError("Bill date must use YYYY-MM-DD format") from exc
        return self._parse_amount_paise(bill_input.amount_rupees)

    def _parse_amount_paise(self, amount_rupees: str) -> int:
        try:
            amount = Decimal(amount_rupees.strip())
        except (InvalidOperation, AttributeError) as exc:
            raise ValidationError("Amount is invalid") from exc
        if amount <= 0:
            raise ValidationError("Amount must be greater than zero")
        return int((amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

    def _require(self, session: UserSession) -> None:
        if not session.has_permission(PermissionCode.BILLING_MANAGE.value):
            raise AuthorizationError(
                f"Missing permission: {PermissionCode.BILLING_MANAGE.value}"
            )
