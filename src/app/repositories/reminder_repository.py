"""
File Purpose: Reminder query operations.
Module: app.repositories.reminder_repository
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: datetime, typing, app.database.connection, app.models.reminder.
"""

from datetime import date
from typing import List, Optional

from app.database.connection import DatabaseConnectionManager
from app.models.reminder import WorkReminder


class ReminderRepository:
    """Repository for due-date reminder queries."""

    def __init__(self, connection_manager: DatabaseConnectionManager) -> None:
        self._connection_manager = connection_manager

    def list_due_work(
        self,
        today: date,
        upcoming_days: int,
        assigned_user_id: Optional[int] = None,
    ) -> List[WorkReminder]:
        """Return overdue and upcoming incomplete work."""

        query = """
            SELECT
                work_items.id,
                work_items.title,
                clients.client_name,
                assigned_to.full_name AS assigned_to_name,
                work_items.status,
                work_items.due_date
            FROM work_items
            JOIN clients ON clients.id = work_items.client_id
            JOIN users AS assigned_to ON assigned_to.id = work_items.assigned_to_user_id
            WHERE work_items.due_date IS NOT NULL
              AND work_items.status NOT IN ('completed', 'cancelled')
              AND work_items.due_date <= date(?, '+' || ? || ' days')
        """
        params = [today.isoformat(), upcoming_days]
        if assigned_user_id is not None:
            query += " AND work_items.assigned_to_user_id = ?"
            params.append(assigned_user_id)
        query += " ORDER BY work_items.due_date ASC, work_items.id ASC;"

        with self._connection_manager.connect() as connection:
            rows = connection.execute(query, tuple(params)).fetchall()

        reminders = []
        for row in rows:
            due_date = date.fromisoformat(str(row["due_date"]))
            days_delta = (due_date - today).days
            reminders.append(
                WorkReminder(
                    work_item_id=int(row["id"]),
                    title=str(row["title"]),
                    client_name=str(row["client_name"]),
                    assigned_to_name=str(row["assigned_to_name"]),
                    status=str(row["status"]),
                    due_date=str(row["due_date"]),
                    reminder_type="overdue" if days_delta < 0 else "upcoming",
                    days_delta=days_delta,
                )
            )
        return reminders
