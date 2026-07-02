"""
File Purpose: Controller for backup UI workflows.
Module: app.controllers.backup_controller
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.core.exceptions, app.models, app.services.
"""

from typing import List, Optional, Tuple

from app.core.exceptions import CAOfficeCMSError
from app.models.backup import BackupFile, BackupResult
from app.models.session import UserSession
from app.services.backup_service import BackupService


class BackupController:
    """Coordinates backup UI actions with service logic."""

    def __init__(self, backup_service: BackupService, session: UserSession) -> None:
        self._backup_service = backup_service
        self._session = session

    def list_backups(self) -> List[BackupFile]:
        """Return available backups."""

        return self._backup_service.list_backups(self._session)

    def create_backup(self) -> Tuple[Optional[BackupResult], Optional[str]]:
        """Create a backup and return an error message on failure."""

        try:
            return self._backup_service.create_backup(self._session), None
        except CAOfficeCMSError as exc:
            return None, str(exc)

    def cleanup_old_backups(self, keep_latest: int = 10) -> Optional[str]:
        """Cleanup old backups and return an error message on failure."""

        try:
            self._backup_service.cleanup_old_backups(self._session, keep_latest)
        except CAOfficeCMSError as exc:
            return str(exc)
        return None
