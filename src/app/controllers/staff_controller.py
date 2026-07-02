"""
File Purpose: Controller for staff management UI workflows.
Module: app.controllers.staff_controller
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.core.exceptions, app.models, app.services.
"""

from typing import List, Optional

from app.core.exceptions import CAOfficeCMSError
from app.models.session import UserSession
from app.models.staff import StaffInput
from app.models.user import User
from app.services.staff_service import StaffService


class StaffController:
    """Coordinates staff UI actions with service logic."""

    def __init__(self, staff_service: StaffService, session: UserSession) -> None:
        self._staff_service = staff_service
        self._session = session

    def list_staff(self, search_text: str = "") -> List[User]:
        """Return staff users visible for management."""

        return self._staff_service.list_staff(self._session, search_text)

    def create(self, staff_input: StaffInput) -> Optional[str]:
        """Create a user and return an error message on failure."""

        try:
            self._staff_service.create_staff(self._session, staff_input)
        except (CAOfficeCMSError, ValueError) as exc:
            return str(exc)
        return None

    def activate(self, user_id: int) -> Optional[str]:
        """Activate a user account and return an error message on failure."""

        try:
            self._staff_service.activate_staff(self._session, user_id)
        except CAOfficeCMSError as exc:
            return str(exc)
        return None

    def deactivate(self, user_id: int) -> Optional[str]:
        """Deactivate a user account and return an error message on failure."""

        try:
            self._staff_service.deactivate_staff(self._session, user_id)
        except CAOfficeCMSError as exc:
            return str(exc)
        return None
