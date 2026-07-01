"""
File Purpose: Controller for dashboard view workflows.
Module: app.controllers.dashboard_controller
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: app.models, app.services.dashboard_service.
"""

from app.models.dashboard import DashboardSummary
from app.models.session import UserSession
from app.services.dashboard_service import DashboardService


class DashboardController:
    """Coordinates dashboard UI with dashboard service logic."""

    def __init__(
        self,
        dashboard_service: DashboardService,
        session: UserSession,
    ) -> None:
        self._dashboard_service = dashboard_service
        self._session = session

    def get_summary(self) -> DashboardSummary:
        """Return dashboard summary for the current session."""

        return self._dashboard_service.get_summary(self._session)

