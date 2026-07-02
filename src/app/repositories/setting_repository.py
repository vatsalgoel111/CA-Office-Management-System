"""
File Purpose: Settings persistence operations.
Module: app.repositories.setting_repository
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.database.connection, app.models.setting.
"""

from typing import List, Optional

from app.database.connection import DatabaseConnectionManager
from app.models.setting import Setting


class SettingRepository:
    """Repository for application settings."""

    def __init__(self, connection_manager: DatabaseConnectionManager) -> None:
        self._connection_manager = connection_manager

    def list_settings(self) -> List[Setting]:
        """List all settings."""

        with self._connection_manager.connect() as connection:
            rows = connection.execute(
                """
                SELECT id, setting_key, setting_value, updated_at
                FROM settings
                ORDER BY setting_key ASC;
                """
            ).fetchall()
        return [self._map_setting(row) for row in rows]

    def get(self, key: str) -> Optional[Setting]:
        """Return a setting by key."""

        with self._connection_manager.connect() as connection:
            row = connection.execute(
                """
                SELECT id, setting_key, setting_value, updated_at
                FROM settings
                WHERE setting_key = ?;
                """,
                (key.strip(),),
            ).fetchone()
        return self._map_setting(row) if row is not None else None

    def upsert(self, key: str, value: str) -> None:
        """Create or update a setting."""

        with self._connection_manager.transaction() as connection:
            connection.execute(
                """
                INSERT INTO settings (setting_key, setting_value)
                VALUES (?, ?)
                ON CONFLICT(setting_key)
                DO UPDATE SET
                    setting_value = excluded.setting_value,
                    updated_at = CURRENT_TIMESTAMP;
                """,
                (key.strip(), value.strip()),
            )

    def _map_setting(self, row) -> Setting:
        return Setting(
            id=int(row["id"]),
            key=str(row["setting_key"]),
            value=str(row["setting_value"]),
            updated_at=str(row["updated_at"]),
        )
