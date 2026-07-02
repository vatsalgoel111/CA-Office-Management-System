"""
File Purpose: Audit log domain models.
Module: app.models.audit
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: dataclasses, typing.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AuditLogEntry:
    """Read-only audit log record."""

    id: int
    user_id: Optional[int]
    username: Optional[str]
    action: str
    entity_type: str
    entity_id: Optional[int]
    old_values: Optional[str]
    new_values: Optional[str]
    description: str
    created_at: str


@dataclass(frozen=True)
class AuditLogInput:
    """Input data for recording an audit event."""

    action: str
    entity_type: str
    description: str
    entity_id: Optional[int] = None
    old_values: Optional[str] = None
    new_values: Optional[str] = None
