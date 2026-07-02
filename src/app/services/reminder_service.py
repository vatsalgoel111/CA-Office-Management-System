"""
File Purpose: Reminder business logic and permission checks.
Module: app.services.reminder_service
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: datetime, app.constants, app.core.exceptions, app.models, app.repositories.
"""

from datetime import date
from typing import Optional

from app.constants import PermissionCode
from app.core.exceptions import AuthorizationError, ValidationError
from app.models.reminder import ReminderSummary
from app.models.session import UserSession
from app.repositories.reminder_repository import ReminderRepository


class ReminderService:
    """Business logic for work reminders."""

    def __init__(self, reminder_repository: ReminderRepository) -> None:
        self._reminder_repository = reminder_repository

    def get_summary(
        self,
        session: UserSession,
        today: Optional[date] = None,
        upcoming_days: int = 7,
    ) -> ReminderSummary:
        """Return reminder summary scoped to the current user."""

        if upcoming_days < 0 or upcoming_days > 90:
            raise ValidationError("Upcoming days must be between 0 and 90")
        assigned_user_id = None
        if session.has_permission(PermissionCode.WORK_VIEW_ALL.value):
            assigned_user_id = None
        elif session.has_permission(PermissionCode.WORK_VIEW_ASSIGNED.value):
            assigned_user_id = session.user.id
        else:
            raise AuthorizationError(
                f"Missing permission: {PermissionCode.WORK_VIEW_ASSIGNED.value}"
            )

        current_date = today or date.today()
        reminders = tuple(
            self._reminder_repository.list_due_work(
                current_date,
                upcoming_days,
                assigned_user_id,
            )
        )
        return ReminderSummary(
            overdue_count=sum(1 for reminder in reminders if reminder.reminder_type == "overdue"),
            upcoming_count=sum(1 for reminder in reminders if reminder.reminder_type == "upcoming"),
            reminders=reminders,
        )
