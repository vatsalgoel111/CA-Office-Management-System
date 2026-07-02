"""
File Purpose: Work item and remark persistence operations.
Module: app.repositories.work_repository
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: datetime, typing, app.database.connection, app.models.work.
"""

from datetime import datetime
from typing import List, Optional

from app.database.connection import DatabaseConnectionManager
from app.models.work import WorkAssignmentInput, WorkItem


class WorkRepository:
    """Repository for work item records."""

    def __init__(self, connection_manager: DatabaseConnectionManager) -> None:
        self._connection_manager = connection_manager

    def create(self, assigned_by_user_id: int, work_input: WorkAssignmentInput) -> int:
        """Create a work item and return its ID."""

        with self._connection_manager.transaction() as connection:
            cursor = connection.execute(
                """
                INSERT INTO work_items (
                    client_id,
                    assigned_to_user_id,
                    assigned_by_user_id,
                    work_type,
                    title,
                    description,
                    priority,
                    status,
                    due_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?);
                """,
                (
                    work_input.client_id,
                    work_input.assigned_to_user_id,
                    assigned_by_user_id,
                    work_input.work_type.strip(),
                    work_input.title.strip(),
                    self._clean(work_input.description),
                    work_input.priority,
                    self._clean(work_input.due_date),
                ),
            )
            return int(cursor.lastrowid)

    def list_work_items(self, assigned_user_id: Optional[int] = None) -> List[WorkItem]:
        """List work items, optionally scoped to one assigned user."""

        query = """
            SELECT
                work_items.id,
                work_items.client_id,
                clients.client_name,
                work_items.assigned_to_user_id,
                assigned_to.full_name AS assigned_to_name,
                work_items.assigned_by_user_id,
                work_items.work_type,
                work_items.title,
                work_items.description,
                work_items.priority,
                work_items.status,
                work_items.due_date,
                work_items.completed_at
            FROM work_items
            JOIN clients ON clients.id = work_items.client_id
            JOIN users AS assigned_to ON assigned_to.id = work_items.assigned_to_user_id
        """
        params = ()
        if assigned_user_id is not None:
            query += " WHERE work_items.assigned_to_user_id = ?"
            params = (assigned_user_id,)
        query += " ORDER BY work_items.due_date IS NULL, work_items.due_date ASC, work_items.id DESC;"

        with self._connection_manager.connect() as connection:
            rows = connection.execute(query, params).fetchall()
        return [self._map_work_item(row) for row in rows]

    def get_by_id(self, work_item_id: int) -> Optional[WorkItem]:
        """Return a work item by ID."""

        with self._connection_manager.connect() as connection:
            row = connection.execute(
                """
                SELECT
                    work_items.id,
                    work_items.client_id,
                    clients.client_name,
                    work_items.assigned_to_user_id,
                    assigned_to.full_name AS assigned_to_name,
                    work_items.assigned_by_user_id,
                    work_items.work_type,
                    work_items.title,
                    work_items.description,
                    work_items.priority,
                    work_items.status,
                    work_items.due_date,
                    work_items.completed_at
                FROM work_items
                JOIN clients ON clients.id = work_items.client_id
                JOIN users AS assigned_to ON assigned_to.id = work_items.assigned_to_user_id
                WHERE work_items.id = ?;
                """,
                (work_item_id,),
            ).fetchone()
        return self._map_work_item(row) if row is not None else None

    def update_status(self, work_item_id: int, status: str) -> None:
        """Update work item status."""

        completed_at = datetime.now().isoformat(timespec="seconds") if status == "completed" else None
        with self._connection_manager.transaction() as connection:
            connection.execute(
                """
                UPDATE work_items
                SET status = ?,
                    completed_at = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?;
                """,
                (status, completed_at, work_item_id),
            )

    def add_remark(self, work_item_id: int, user_id: int, remark_text: str) -> int:
        """Add a remark to a work item."""

        with self._connection_manager.transaction() as connection:
            cursor = connection.execute(
                """
                INSERT INTO remarks (work_item_id, user_id, remark_text)
                VALUES (?, ?, ?);
                """,
                (work_item_id, user_id, remark_text.strip()),
            )
            return int(cursor.lastrowid)

    def count_remarks(self, work_item_id: int) -> int:
        """Return remark count for a work item."""

        with self._connection_manager.connect() as connection:
            return int(
                connection.execute(
                    "SELECT COUNT(*) FROM remarks WHERE work_item_id = ?;",
                    (work_item_id,),
                ).fetchone()[0]
            )

    def _clean(self, value: str) -> Optional[str]:
        cleaned = value.strip()
        return cleaned or None

    def _map_work_item(self, row) -> WorkItem:
        return WorkItem(
            id=int(row["id"]),
            client_id=int(row["client_id"]),
            client_name=str(row["client_name"]),
            assigned_to_user_id=int(row["assigned_to_user_id"]),
            assigned_to_name=str(row["assigned_to_name"]),
            assigned_by_user_id=int(row["assigned_by_user_id"]),
            work_type=str(row["work_type"]),
            title=str(row["title"]),
            description=row["description"],
            priority=str(row["priority"]),
            status=str(row["status"]),
            due_date=row["due_date"],
            completed_at=row["completed_at"],
        )

