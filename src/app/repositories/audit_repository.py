"""
File Purpose: Audit log persistence operations.
Module: app.repositories.audit_repository
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.database.connection, app.models.audit.
"""

from typing import List, Optional

from app.database.connection import DatabaseConnectionManager
from app.models.audit import AuditLogEntry, AuditLogInput


class AuditRepository:
    """Repository for append-only audit log records."""

    def __init__(self, connection_manager: DatabaseConnectionManager) -> None:
        self._connection_manager = connection_manager

    def create(self, user_id: Optional[int], audit_input: AuditLogInput) -> int:
        """Create an audit log entry and return its ID."""

        with self._connection_manager.transaction() as connection:
            cursor = connection.execute(
                """
                INSERT INTO audit_logs (
                    user_id,
                    action,
                    entity_type,
                    entity_id,
                    old_values,
                    new_values,
                    description
                )
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    user_id,
                    audit_input.action.strip().lower(),
                    audit_input.entity_type.strip().lower(),
                    audit_input.entity_id,
                    audit_input.old_values,
                    audit_input.new_values,
                    audit_input.description.strip(),
                ),
            )
            return int(cursor.lastrowid)

    def list_entries(self, search_text: str = "", limit: int = 200) -> List[AuditLogEntry]:
        """List recent audit entries."""

        query = """
            SELECT
                audit_logs.id,
                audit_logs.user_id,
                users.username,
                audit_logs.action,
                audit_logs.entity_type,
                audit_logs.entity_id,
                audit_logs.old_values,
                audit_logs.new_values,
                audit_logs.description,
                audit_logs.created_at
            FROM audit_logs
            LEFT JOIN users ON users.id = audit_logs.user_id
        """
        params = []
        cleaned_search = search_text.strip().lower()
        if cleaned_search:
            query += """
                WHERE LOWER(audit_logs.action) LIKE ?
                   OR LOWER(audit_logs.entity_type) LIKE ?
                   OR LOWER(audit_logs.description) LIKE ?
                   OR LOWER(users.username) LIKE ?
            """
            search_pattern = f"%{cleaned_search}%"
            params.extend([search_pattern] * 4)
        query += " ORDER BY audit_logs.created_at DESC, audit_logs.id DESC LIMIT ?;"
        params.append(limit)

        with self._connection_manager.connect() as connection:
            rows = connection.execute(query, tuple(params)).fetchall()
        return [self._map_entry(row) for row in rows]

    def _map_entry(self, row) -> AuditLogEntry:
        return AuditLogEntry(
            id=int(row["id"]),
            user_id=row["user_id"],
            username=row["username"],
            action=str(row["action"]),
            entity_type=str(row["entity_type"]),
            entity_id=row["entity_id"],
            old_values=row["old_values"],
            new_values=row["new_values"],
            description=str(row["description"]),
            created_at=str(row["created_at"]),
        )
