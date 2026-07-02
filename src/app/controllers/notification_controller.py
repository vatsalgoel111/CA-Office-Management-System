"""
File Purpose: Controller for notification queue UI workflows.
Module: app.controllers.notification_controller
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.core.exceptions, app.models, app.services.
"""

from typing import List, Optional

from app.core.exceptions import CAOfficeCMSError
from app.models.notification import NotificationInput, NotificationRecord
from app.models.session import UserSession
from app.services.notification_service import NotificationService


class NotificationController:
    """Coordinates notification UI actions with service logic."""

    def __init__(self, notification_service: NotificationService, session: UserSession) -> None:
        self._notification_service = notification_service
        self._session = session

    def list_notifications(self) -> List[NotificationRecord]:
        """Return queued notifications."""

        return self._notification_service.list_notifications(self._session)

    def queue(self, notification_input: NotificationInput) -> Optional[str]:
        """Queue a notification and return an error message on failure."""

        try:
            self._notification_service.queue_notification(self._session, notification_input)
        except CAOfficeCMSError as exc:
            return str(exc)
        return None
