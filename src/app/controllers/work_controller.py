"""
File Purpose: Controller for work management UI workflows.
Module: app.controllers.work_controller
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.core.exceptions, app.models, app.services.
"""

from typing import List, Optional

from app.core.exceptions import CAOfficeCMSError
from app.models.session import UserSession
from app.models.work import WorkAssignmentInput, WorkItem
from app.services.work_service import WorkService


class WorkController:
    """Coordinates work UI actions with service logic."""

    def __init__(self, work_service: WorkService, session: UserSession) -> None:
        self._work_service = work_service
        self._session = session

    def list_work(self) -> List[WorkItem]:
        """Return visible work items."""

        return self._work_service.list_work(self._session)

    def assign(self, work_input: WorkAssignmentInput) -> Optional[str]:
        """Assign work and return an error message on failure."""

        try:
            self._work_service.assign_work(self._session, work_input)
        except CAOfficeCMSError as exc:
            return str(exc)
        return None

    def update_status(
        self,
        work_item_id: int,
        status: str,
        remark: str = "",
    ) -> Optional[str]:
        """Update work status and return an error message on failure."""

        try:
            self._work_service.update_status(
                self._session,
                work_item_id,
                status,
                remark,
            )
        except CAOfficeCMSError as exc:
            return str(exc)
        return None

