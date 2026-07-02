"""
File Purpose: Controller for audit log UI workflows.
Module: app.controllers.audit_controller
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.core.exceptions, app.models, app.services.
"""

from typing import List

from app.models.audit import AuditLogEntry
from app.models.session import UserSession
from app.services.audit_service import AuditService


class AuditController:
    """Coordinates audit UI actions with service logic."""

    def __init__(self, audit_service: AuditService, session: UserSession) -> None:
        self._audit_service = audit_service
        self._session = session

    def list_entries(self, search_text: str = "") -> List[AuditLogEntry]:
        """Return recent audit entries."""

        return self._audit_service.list_entries(self._session, search_text)
