"""
File Purpose: Dashboard summary business logic.
Module: app.services.dashboard_service
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: datetime, typing, app.constants, app.models, app.repositories.
"""

from datetime import date
from typing import Optional

from app.constants import PermissionCode
from app.models.dashboard import DashboardSummary
from app.models.session import UserSession
from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:
    """Build dashboard summaries for authenticated users."""

    def __init__(self, dashboard_repository: DashboardRepository) -> None:
        self._dashboard_repository = dashboard_repository

    def get_summary(
        self,
        session: UserSession,
        today: Optional[date] = None,
    ) -> DashboardSummary:
        """Return dashboard summary for the current session."""

        current_date = today or date.today()
        assigned_user_id = None
        if not session.has_permission(PermissionCode.WORK_VIEW_ALL.value):
            assigned_user_id = session.user.id

        return DashboardSummary(
            active_clients=self._dashboard_repository.count_active_clients(),
            pending_work=self._dashboard_repository.count_pending_work(assigned_user_id),
            overdue_work=self._dashboard_repository.count_overdue_work(
                current_date,
                assigned_user_id,
            ),
            completed_work=self._dashboard_repository.count_completed_work(
                assigned_user_id
            ),
            unpaid_bills=self._dashboard_repository.count_unpaid_bills(),
            outstanding_amount_paise=(
                self._dashboard_repository.calculate_outstanding_amount_paise()
            ),
        )
