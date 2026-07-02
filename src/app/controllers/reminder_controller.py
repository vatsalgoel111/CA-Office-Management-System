"""
File Purpose: Controller for reminder UI workflows.
Module: app.controllers.reminder_controller
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: app.models, app.services.
"""

from app.models.reminder import ReminderSummary
from app.models.session import UserSession
from app.services.reminder_service import ReminderService


class ReminderController:
    """Coordinates reminder UI actions with service logic."""

    def __init__(self, reminder_service: ReminderService, session: UserSession) -> None:
        self._reminder_service = reminder_service
        self._session = session

    def get_summary(self) -> ReminderSummary:
        """Return current reminder summary."""

        return self._reminder_service.get_summary(self._session)
