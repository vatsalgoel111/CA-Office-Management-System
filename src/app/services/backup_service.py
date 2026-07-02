"""
File Purpose: SQLite backup and retention business logic.
Module: app.services.backup_service
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: datetime, sqlite3, typing, app.constants, app.core, app.models.
"""

from datetime import datetime
import sqlite3
from typing import List

from app.constants import PermissionCode
from app.core.exceptions import AuthorizationError, ValidationError
from app.core.paths import AppPaths
from app.models.backup import BackupFile, BackupResult
from app.models.session import UserSession


class BackupService:
    """Business logic for local SQLite database backups."""

    def __init__(self, paths: AppPaths) -> None:
        self._paths = paths

    def create_backup(self, session: UserSession) -> BackupResult:
        """Create a verified SQLite backup."""

        self._require(session)
        if not self._paths.database_file.exists():
            raise ValidationError("Database file does not exist")

        self._paths.backups_dir.mkdir(parents=True, exist_ok=True)
        backup_path = self._paths.backups_dir / self._build_filename()
        source = sqlite3.connect(str(self._paths.database_file))
        destination = sqlite3.connect(str(backup_path))
        try:
            source.backup(destination)
        finally:
            destination.close()
            source.close()

        integrity_ok = self.verify_backup(backup_path)
        return BackupResult(
            file_path=backup_path,
            size_bytes=backup_path.stat().st_size,
            integrity_ok=integrity_ok,
        )

    def list_backups(self, session: UserSession) -> List[BackupFile]:
        """List local backup files."""

        self._require(session)
        if not self._paths.backups_dir.exists():
            return []
        backups = []
        for file_path in self._paths.backups_dir.glob("ca_office_cms_backup_*.sqlite3"):
            stat = file_path.stat()
            backups.append(
                BackupFile(
                    file_path=file_path,
                    size_bytes=stat.st_size,
                    created_at=datetime.fromtimestamp(stat.st_mtime).isoformat(
                        timespec="seconds"
                    ),
                )
            )
        return sorted(backups, key=lambda backup: backup.created_at, reverse=True)

    def cleanup_old_backups(self, session: UserSession, keep_latest: int = 10) -> int:
        """Delete old backup files after keeping the newest backups."""

        self._require(session)
        if keep_latest <= 0:
            raise ValidationError("At least one backup must be retained")
        backups = self.list_backups(session)
        deleted_count = 0
        for backup in backups[keep_latest:]:
            backup.file_path.unlink(missing_ok=True)
            deleted_count += 1
        return deleted_count

    def verify_backup(self, backup_path) -> bool:
        """Return whether a backup passes SQLite integrity check."""

        connection = sqlite3.connect(str(backup_path))
        try:
            result = connection.execute("PRAGMA integrity_check;").fetchone()[0]
            return result == "ok"
        finally:
            connection.close()

    def _build_filename(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"ca_office_cms_backup_{timestamp}.sqlite3"

    def _require(self, session: UserSession) -> None:
        if not session.has_permission(PermissionCode.BACKUP_CREATE.value):
            raise AuthorizationError(
                f"Missing permission: {PermissionCode.BACKUP_CREATE.value}"
            )
