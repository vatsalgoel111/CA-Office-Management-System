"""
File Purpose: Shared lookup queries for UI selectors.
Module: app.repositories.lookup_repository
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.database.connection, app.models.lookup.
"""

from typing import List

from app.database.connection import DatabaseConnectionManager
from app.models.lookup import LookupChoice


class LookupRepository:
    """Repository for lightweight selector lookup data."""

    def __init__(self, connection_manager: DatabaseConnectionManager) -> None:
        self._connection_manager = connection_manager

    def active_clients(self) -> List[LookupChoice]:
        """Return active client choices."""

        with self._connection_manager.connect() as connection:
            rows = connection.execute(
                """
                SELECT id, client_name, COALESCE(business_name, '') AS business_name
                FROM clients
                WHERE status = 'active'
                ORDER BY client_name ASC;
                """
            ).fetchall()
        return [
            LookupChoice(
                id=int(row["id"]),
                label=self._join_label(row["client_name"], row["business_name"]),
            )
            for row in rows
        ]

    def active_users(self) -> List[LookupChoice]:
        """Return active user choices."""

        with self._connection_manager.connect() as connection:
            rows = connection.execute(
                """
                SELECT users.id, users.full_name, roles.name AS role_name
                FROM users
                JOIN roles ON roles.id = users.role_id
                WHERE users.is_active = 1
                ORDER BY users.full_name ASC;
                """
            ).fetchall()
        return [
            LookupChoice(
                id=int(row["id"]),
                label=self._join_label(row["full_name"], row["role_name"]),
            )
            for row in rows
        ]

    def work_items(self) -> List[LookupChoice]:
        """Return work item choices."""

        with self._connection_manager.connect() as connection:
            rows = connection.execute(
                """
                SELECT work_items.id, work_items.title, clients.client_name
                FROM work_items
                JOIN clients ON clients.id = work_items.client_id
                WHERE work_items.status NOT IN ('completed', 'cancelled')
                ORDER BY work_items.due_date IS NULL, work_items.due_date ASC;
                """
            ).fetchall()
        return [
            LookupChoice(
                id=int(row["id"]),
                label=self._join_label(row["title"], row["client_name"]),
            )
            for row in rows
        ]

    def open_bills(self) -> List[LookupChoice]:
        """Return unpaid or partially paid bill choices."""

        with self._connection_manager.connect() as connection:
            rows = connection.execute(
                """
                SELECT bills.id, bills.bill_number, clients.client_name
                FROM bills
                JOIN clients ON clients.id = bills.client_id
                WHERE bills.status IN ('unpaid', 'partial')
                ORDER BY bills.bill_date ASC, bills.id ASC;
                """
            ).fetchall()
        return [
            LookupChoice(
                id=int(row["id"]),
                label=self._join_label(row["bill_number"], row["client_name"]),
            )
            for row in rows
        ]

    def _join_label(self, primary: str, secondary: str) -> str:
        secondary = str(secondary or "").strip()
        return f"{primary} - {secondary}" if secondary else str(primary)
