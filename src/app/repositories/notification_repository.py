"""
File Purpose: Notification queue persistence operations.
Module: app.repositories.notification_repository
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.database.connection, app.models.notification.
"""

from typing import List

from app.database.connection import DatabaseConnectionManager
from app.models.notification import NotificationInput, NotificationRecord


class NotificationRepository:
    """Repository for notification queue records."""

    def __init__(self, connection_manager: DatabaseConnectionManager) -> None:
        self._connection_manager = connection_manager

    def create(self, notification_input: NotificationInput) -> int:
        """Create a queued notification."""

        with self._connection_manager.transaction() as connection:
            cursor = connection.execute(
                """
                INSERT INTO notifications (
                    recipient_user_id,
                    related_work_item_id,
                    notification_type,
                    provider,
                    message,
                    status
                )
                VALUES (?, ?, ?, ?, ?, 'pending');
                """,
                (
                    notification_input.recipient_user_id,
                    notification_input.related_work_item_id,
                    notification_input.notification_type.strip().lower(),
                    notification_input.provider.strip().lower(),
                    notification_input.message.strip(),
                ),
            )
            return int(cursor.lastrowid)

    def list_notifications(self, status: str = "") -> List[NotificationRecord]:
        """List queued notifications."""

        query = """
            SELECT
                notifications.id,
                notifications.recipient_user_id,
                users.full_name AS recipient_name,
                notifications.related_work_item_id,
                notifications.notification_type,
                notifications.provider,
                notifications.message,
                notifications.status,
                notifications.failure_reason,
                notifications.retry_count,
                notifications.sent_at,
                notifications.created_at
            FROM notifications
            JOIN users ON users.id = notifications.recipient_user_id
        """
        params = []
        if status.strip():
            query += " WHERE notifications.status = ?"
            params.append(status.strip().lower())
        query += " ORDER BY notifications.created_at DESC, notifications.id DESC;"

        with self._connection_manager.connect() as connection:
            rows = connection.execute(query, tuple(params)).fetchall()
        return [self._map_notification(row) for row in rows]

    def user_exists(self, user_id: int) -> bool:
        """Return whether an active user exists."""

        with self._connection_manager.connect() as connection:
            count = connection.execute(
                "SELECT COUNT(*) FROM users WHERE id = ? AND is_active = 1;",
                (user_id,),
            ).fetchone()[0]
        return int(count) > 0

    def work_item_exists(self, work_item_id: int) -> bool:
        """Return whether a work item exists."""

        with self._connection_manager.connect() as connection:
            count = connection.execute(
                "SELECT COUNT(*) FROM work_items WHERE id = ?;",
                (work_item_id,),
            ).fetchone()[0]
        return int(count) > 0

    def mark_sent(self, notification_id: int) -> None:
        """Mark a notification as sent."""

        with self._connection_manager.transaction() as connection:
            connection.execute(
                """
                UPDATE notifications
                SET status = 'sent',
                    sent_at = CURRENT_TIMESTAMP
                WHERE id = ?;
                """,
                (notification_id,),
            )

    def _map_notification(self, row) -> NotificationRecord:
        return NotificationRecord(
            id=int(row["id"]),
            recipient_user_id=int(row["recipient_user_id"]),
            recipient_name=str(row["recipient_name"]),
            related_work_item_id=row["related_work_item_id"],
            notification_type=str(row["notification_type"]),
            provider=str(row["provider"]),
            message=str(row["message"]),
            status=str(row["status"]),
            failure_reason=row["failure_reason"],
            retry_count=int(row["retry_count"]),
            sent_at=row["sent_at"],
            created_at=str(row["created_at"]),
        )
