"""
File Purpose: Dashboard summary domain models.
Module: app.models.dashboard
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: dataclasses.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DashboardSummary:
    """Dashboard summary values for the authenticated user."""

    active_clients: int
    pending_work: int
    overdue_work: int
    completed_work: int
    unpaid_bills: int
    outstanding_amount_paise: int

    @property
    def outstanding_amount_rupees(self) -> str:
        """Return outstanding amount formatted in rupees."""

        rupees = self.outstanding_amount_paise / 100
        return f"Rs. {rupees:,.2f}"

