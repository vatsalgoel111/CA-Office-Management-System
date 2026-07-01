"""
File Purpose: Session model for authenticated users.
Module: app.models.session
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: dataclasses, typing, app.models.user.
"""

from dataclasses import dataclass
from typing import FrozenSet

from app.models.user import User


@dataclass(frozen=True)
class UserSession:
    """Authenticated user session with resolved permissions."""

    user: User
    permissions: FrozenSet[str]

    def has_permission(self, permission_code: str) -> bool:
        """Return whether the session has a permission code."""

        return permission_code in self.permissions

