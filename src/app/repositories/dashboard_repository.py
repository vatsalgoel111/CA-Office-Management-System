"""
File Purpose: Dashboard metric persistence queries.
Module: app.repositories.dashboard_repository
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: datetime, typing, app.database.connection.
"""

from datetime import date
from typing import Optional, Tuple

from app.database.connection import DatabaseConnectionManager


class DashboardRepository:
    """Repository for dashboard summary metrics."""

    def __init__(self, connection_manager: DatabaseConnectionManager) -> None:
        self._connection_manager = connection_manager

    def count_active_clients(self) -> int:
        """Return active client count."""

        return self._count("SELECT COUNT(*) FROM clients WHERE status = 'active';")

    def count_pending_work(self, assigned_user_id: Optional[int] = None) -> int:
        """Return pending/in-progress work count."""

        query = """
            SELECT COUNT(*)
            FROM work_items
            WHERE status IN ('pending', 'in_progress', 'waiting_for_client', 'on_hold')
        """
        params: Tuple[object, ...] = ()
        if assigned_user_id is not None:
            query += " AND assigned_to_user_id = ?"
            params = (assigned_user_id,)
        return self._count(query, params)

    def count_overdue_work(
        self,
        today: date,
        assigned_user_id: Optional[int] = None,
    ) -> int:
        """Return overdue work count."""

        query = """
            SELECT COUNT(*)
            FROM work_items
            WHERE due_date IS NOT NULL
              AND due_date < ?
              AND status NOT IN ('completed', 'cancelled')
        """
        params: Tuple[object, ...] = (today.isoformat(),)
        if assigned_user_id is not None:
            query += " AND assigned_to_user_id = ?"
            params = (today.isoformat(), assigned_user_id)
        return self._count(query, params)

    def count_completed_work(self, assigned_user_id: Optional[int] = None) -> int:
        """Return completed work count."""

        query = "SELECT COUNT(*) FROM work_items WHERE status = 'completed'"
        params: Tuple[object, ...] = ()
        if assigned_user_id is not None:
            query += " AND assigned_to_user_id = ?"
            params = (assigned_user_id,)
        return self._count(query, params)

    def count_unpaid_bills(self) -> int:
        """Return unpaid or partially-paid bill count."""

        return self._count(
            "SELECT COUNT(*) FROM bills WHERE status IN ('unpaid', 'partial');"
        )

    def calculate_outstanding_amount_paise(self) -> int:
        """Return total outstanding amount in paise."""

        query = """
            SELECT
                COALESCE(SUM(bills.amount_paise), 0)
                - COALESCE(SUM(collection_totals.received_amount_paise), 0)
                    AS outstanding_amount_paise
            FROM bills
            LEFT JOIN (
                SELECT bill_id, SUM(received_amount_paise) AS received_amount_paise
                FROM collections
                GROUP BY bill_id
            ) AS collection_totals ON collection_totals.bill_id = bills.id
            WHERE bills.status IN ('unpaid', 'partial');
        """
        with self._connection_manager.connect() as connection:
            value = connection.execute(query).fetchone()[0]
        return max(int(value or 0), 0)

    def _count(self, query: str, params: Tuple[object, ...] = ()) -> int:
        with self._connection_manager.connect() as connection:
            return int(connection.execute(query, params).fetchone()[0])
