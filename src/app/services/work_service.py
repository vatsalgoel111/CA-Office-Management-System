"""
File Purpose: Work assignment and status business logic.
Module: app.services.work_service
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: datetime, typing, app.constants, app.core.exceptions, app.models, app.repositories.
"""

from datetime import date
from typing import List

from app.constants import PermissionCode
from app.core.exceptions import AuthorizationError, ValidationError
from app.models.session import UserSession
from app.models.work import WorkAssignmentInput, WorkItem
from app.repositories.work_repository import WorkRepository


VALID_PRIORITIES = {"low", "normal", "high", "urgent"}
VALID_STATUSES = {
    "pending",
    "in_progress",
    "waiting_for_client",
    "completed",
    "on_hold",
    "cancelled",
}


class WorkService:
    """Business logic for work management."""

    def __init__(self, work_repository: WorkRepository) -> None:
        self._work_repository = work_repository

    def assign_work(self, session: UserSession, work_input: WorkAssignmentInput) -> int:
        """Assign work to a user."""

        self._require(session, PermissionCode.WORK_ASSIGN.value)
        self._validate_assignment(work_input)
        return self._work_repository.create(session.user.id, work_input)

    def list_work(self, session: UserSession) -> List[WorkItem]:
        """List work visible to the current user."""

        if session.has_permission(PermissionCode.WORK_VIEW_ALL.value):
            return self._work_repository.list_work_items()
        self._require(session, PermissionCode.WORK_VIEW_ASSIGNED.value)
        return self._work_repository.list_work_items(session.user.id)

    def update_status(
        self,
        session: UserSession,
        work_item_id: int,
        status: str,
        remark: str = "",
    ) -> None:
        """Update work status and optionally add a remark."""

        self._require(session, PermissionCode.WORK_UPDATE_STATUS.value)
        normalized_status = status.strip().lower()
        if normalized_status not in VALID_STATUSES:
            raise ValidationError("Invalid work status")

        work_item = self._work_repository.get_by_id(work_item_id)
        if work_item is None:
            raise ValidationError("Work item not found")
        if (
            not session.has_permission(PermissionCode.WORK_VIEW_ALL.value)
            and work_item.assigned_to_user_id != session.user.id
        ):
            raise AuthorizationError("Cannot update work assigned to another user")

        self._work_repository.update_status(work_item_id, normalized_status)
        if remark.strip():
            self._work_repository.add_remark(work_item_id, session.user.id, remark)

    def _validate_assignment(self, work_input: WorkAssignmentInput) -> None:
        if work_input.client_id <= 0:
            raise ValidationError("Client is required")
        if work_input.assigned_to_user_id <= 0:
            raise ValidationError("Assigned staff is required")
        if not work_input.work_type.strip():
            raise ValidationError("Work type is required")
        if not work_input.title.strip():
            raise ValidationError("Work title is required")
        if work_input.priority not in VALID_PRIORITIES:
            raise ValidationError("Invalid work priority")
        if work_input.due_date:
            try:
                date.fromisoformat(work_input.due_date)
            except ValueError as exc:
                raise ValidationError("Due date must use YYYY-MM-DD format") from exc

    def _require(self, session: UserSession, permission_code: str) -> None:
        if not session.has_permission(permission_code):
            raise AuthorizationError(f"Missing permission: {permission_code}")

