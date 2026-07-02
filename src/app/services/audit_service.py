"""
File Purpose: Audit log business logic and permission checks.
Module: app.services.audit_service
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: json, typing, app.constants, app.core.exceptions, app.models, app.repositories.
"""

import json
from typing import Dict, List, Optional

from app.constants import PermissionCode
from app.core.exceptions import AuthorizationError, ValidationError
from app.models.audit import AuditLogEntry, AuditLogInput
from app.models.session import UserSession
from app.repositories.audit_repository import AuditRepository


class AuditService:
    """Business logic for append-only audit logs."""

    def __init__(self, audit_repository: AuditRepository) -> None:
        self._audit_repository = audit_repository

    def record_event(
        self,
        session: Optional[UserSession],
        action: str,
        entity_type: str,
        description: str,
        entity_id: Optional[int] = None,
        old_values: Optional[Dict[str, object]] = None,
        new_values: Optional[Dict[str, object]] = None,
    ) -> int:
        """Record an audit event."""

        audit_input = AuditLogInput(
            action=self._require_text(action, "Action"),
            entity_type=self._require_text(entity_type, "Entity type"),
            entity_id=entity_id,
            old_values=self._encode(old_values),
            new_values=self._encode(new_values),
            description=self._require_text(description, "Description"),
        )
        user_id = session.user.id if session is not None else None
        return self._audit_repository.create(user_id, audit_input)

    def list_entries(
        self,
        session: UserSession,
        search_text: str = "",
        limit: int = 200,
    ) -> List[AuditLogEntry]:
        """List audit entries after permission check."""

        self._require_view(session)
        if limit <= 0 or limit > 1000:
            raise ValidationError("Audit log limit must be between 1 and 1000")
        return self._audit_repository.list_entries(search_text, limit)

    def _encode(self, values: Optional[Dict[str, object]]) -> Optional[str]:
        if values is None:
            return None
        return json.dumps(values, sort_keys=True)

    def _require_text(self, value: str, label: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValidationError(f"{label} is required")
        return cleaned

    def _require_view(self, session: UserSession) -> None:
        if not session.has_permission(PermissionCode.AUDIT_VIEW.value):
            raise AuthorizationError(
                f"Missing permission: {PermissionCode.AUDIT_VIEW.value}"
            )
