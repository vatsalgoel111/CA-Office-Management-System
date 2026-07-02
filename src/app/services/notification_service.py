"""
File Purpose: Notification queue and WhatsApp message preparation logic.
Module: app.services.notification_service
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.constants, app.core.exceptions, app.models, app.repositories.
"""

from typing import List, Optional

from app.constants import PermissionCode
from app.core.exceptions import AuthorizationError, ValidationError
from app.models.notification import NotificationInput, NotificationRecord
from app.models.session import UserSession
from app.repositories.notification_repository import NotificationRepository


VALID_NOTIFICATION_TYPES = {
    "work_assigned",
    "work_updated",
    "daily_pending_summary",
    "overdue_reminder",
    "manual",
}
VALID_PROVIDERS = {"manual", "whatsapp"}


class NotificationService:
    """Business logic for queued notifications."""

    def __init__(self, notification_repository: NotificationRepository) -> None:
        self._notification_repository = notification_repository

    def list_notifications(
        self,
        session: UserSession,
        status: str = "",
    ) -> List[NotificationRecord]:
        """List notifications for administrators/settings managers."""

        self._require_manage(session)
        return self._notification_repository.list_notifications(status)

    def queue_notification(
        self,
        session: UserSession,
        notification_input: NotificationInput,
    ) -> int:
        """Queue a notification after validation."""

        self._require_manage(session)
        self._validate(notification_input)
        return self._notification_repository.create(notification_input)

    def queue_whatsapp_message(
        self,
        session: UserSession,
        recipient_user_id: int,
        message: str,
        notification_type: str = "manual",
        related_work_item_id: Optional[int] = None,
    ) -> int:
        """Queue a WhatsApp notification for later provider delivery."""

        return self.queue_notification(
            session,
            NotificationInput(
                recipient_user_id=recipient_user_id,
                related_work_item_id=related_work_item_id,
                notification_type=notification_type,
                provider="whatsapp",
                message=message,
            ),
        )

    def mark_sent(self, session: UserSession, notification_id: int) -> None:
        """Mark a notification as sent for manual/provider workflows."""

        self._require_manage(session)
        self._notification_repository.mark_sent(notification_id)

    def _validate(self, notification_input: NotificationInput) -> None:
        if notification_input.recipient_user_id <= 0:
            raise ValidationError("Recipient is required")
        if not self._notification_repository.user_exists(
            notification_input.recipient_user_id
        ):
            raise ValidationError("Recipient user not found")
        notification_type = notification_input.notification_type.strip().lower()
        if notification_type not in VALID_NOTIFICATION_TYPES:
            raise ValidationError("Notification type is invalid")
        provider = notification_input.provider.strip().lower()
        if provider not in VALID_PROVIDERS:
            raise ValidationError("Notification provider is invalid")
        if notification_input.related_work_item_id is not None:
            if notification_input.related_work_item_id <= 0:
                raise ValidationError("Related work item is invalid")
            if not self._notification_repository.work_item_exists(
                notification_input.related_work_item_id
            ):
                raise ValidationError("Related work item not found")
        if not notification_input.message.strip():
            raise ValidationError("Message is required")

    def _require_manage(self, session: UserSession) -> None:
        if not session.has_permission(PermissionCode.SETTINGS_MANAGE.value):
            raise AuthorizationError(
                f"Missing permission: {PermissionCode.SETTINGS_MANAGE.value}"
            )
