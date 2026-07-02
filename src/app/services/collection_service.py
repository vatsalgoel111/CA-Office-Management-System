"""
File Purpose: Collection tracking business logic and permission checks.
Module: app.services.collection_service
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
from app.models.collection import CollectionInput, CollectionRecord
from app.models.session import UserSession
from app.repositories.collection_repository import CollectionRepository


VALID_PAYMENT_MODES = {"cash", "bank", "upi", "cheque", "other"}


class CollectionService:
    """Business logic for payment collection tracking."""

    def __init__(self, collection_repository: CollectionRepository) -> None:
        self._collection_repository = collection_repository

    def list_collections(
        self,
        session: UserSession,
        search_text: str = "",
    ) -> List[CollectionRecord]:
        """List collections after permission check."""

        self._require(session)
        return self._collection_repository.list_collections(search_text)

    def record_collection(
        self,
        session: UserSession,
        collection_input: CollectionInput,
    ) -> int:
        """Record a collection and update linked bill status."""

        self._require(session)
        amount_paise, bill_amount_paise = self._validate_collection(collection_input)
        return self._collection_repository.create_and_update_bill_status(
            collection_input,
            amount_paise,
            bill_amount_paise,
        )

    def _validate_collection(self, collection_input: CollectionInput) -> tuple[int, int]:
        if collection_input.bill_id <= 0:
            raise ValidationError("Bill is required")
        bill_financials = self._collection_repository.get_bill_financials(
            collection_input.bill_id
        )
        if bill_financials is None:
            raise ValidationError("Bill not found")
        bill_amount_paise, bill_status = bill_financials
        if bill_status == "cancelled":
            raise ValidationError("Cannot collect against a cancelled bill")
        try:
            date.fromisoformat(collection_input.received_date)
        except ValueError as exc:
            raise ValidationError("Received date must use YYYY-MM-DD format") from exc
        payment_mode = collection_input.payment_mode.strip().lower()
        if payment_mode not in VALID_PAYMENT_MODES:
            raise ValidationError("Payment mode is invalid")
        amount_paise = self._parse_amount_paise(collection_input.received_amount_rupees)
        received_total = self._collection_repository.get_received_total_paise(
            collection_input.bill_id
        )
        outstanding = bill_amount_paise - received_total
        if amount_paise > outstanding:
            raise ValidationError("Collection amount exceeds outstanding balance")
        return amount_paise, bill_amount_paise

    def _parse_amount_paise(self, amount_rupees: str) -> int:
        try:
            amount = Decimal(amount_rupees.strip())
        except (InvalidOperation, AttributeError) as exc:
            raise ValidationError("Collection amount is invalid") from exc
        if amount <= 0:
            raise ValidationError("Collection amount must be greater than zero")
        return int((amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

    def _require(self, session: UserSession) -> None:
        if not session.has_permission(PermissionCode.COLLECTIONS_MANAGE.value):
            raise AuthorizationError(
                f"Missing permission: {PermissionCode.COLLECTIONS_MANAGE.value}"
            )
