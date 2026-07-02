"""
File Purpose: Controller for billing UI workflows.
Module: app.controllers.billing_controller
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.core.exceptions, app.models, app.services.
"""

from typing import List, Optional

from app.core.exceptions import CAOfficeCMSError
from app.models.billing import Bill, BillInput
from app.models.session import UserSession
from app.services.billing_service import BillingService


class BillingController:
    """Coordinates billing UI actions with service logic."""

    def __init__(self, billing_service: BillingService, session: UserSession) -> None:
        self._billing_service = billing_service
        self._session = session

    def list_bills(self, search_text: str = "") -> List[Bill]:
        """Return bills visible for billing users."""

        return self._billing_service.list_bills(self._session, search_text)

    def create(self, bill_input: BillInput) -> Optional[str]:
        """Create a bill and return an error message on failure."""

        try:
            self._billing_service.create_bill(self._session, bill_input)
        except CAOfficeCMSError as exc:
            return str(exc)
        return None

    def update_status(self, bill_id: int, status: str) -> Optional[str]:
        """Update bill status and return an error message on failure."""

        try:
            self._billing_service.update_status(self._session, bill_id, status)
        except CAOfficeCMSError as exc:
            return str(exc)
        return None
