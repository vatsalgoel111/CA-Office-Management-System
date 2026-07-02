"""
File Purpose: Staff account management business logic.
Module: app.services.staff_service
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.constants, app.core, app.models, app.repositories.
"""

from typing import List

from app.constants import PermissionCode, RoleCode
from app.core.exceptions import AuthorizationError, ValidationError
from app.core.security import hash_password
from app.models.session import UserSession
from app.models.staff import StaffInput
from app.models.user import CreateUserRequest, User
from app.repositories.user_repository import UserRepository


class StaffService:
    """Business logic for staff and user account management."""

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def list_staff(
        self,
        session: UserSession,
        search_text: str = "",
        include_inactive: bool = True,
    ) -> List[User]:
        """List staff user accounts."""

        self._require(session, PermissionCode.USERS_MANAGE.value)
        return self._user_repository.list_users(search_text, include_inactive)

    def create_staff(self, session: UserSession, staff_input: StaffInput) -> int:
        """Create a staff user account."""

        self._require(session, PermissionCode.USERS_MANAGE.value)
        self._validate(staff_input)
        if self._user_repository.get_by_username(staff_input.username) is not None:
            raise ValidationError("Username already exists")
        return self._user_repository.create_user(
            CreateUserRequest(
                full_name=staff_input.full_name,
                username=staff_input.username,
                password_hash=hash_password(staff_input.password),
                role_code=staff_input.role_code.strip().lower(),
                mobile=staff_input.mobile.strip() or None,
                email=staff_input.email.strip().lower() or None,
            )
        )

    def activate_staff(self, session: UserSession, user_id: int) -> None:
        """Activate a user account."""

        self._require(session, PermissionCode.USERS_MANAGE.value)
        self._ensure_user_exists(user_id)
        self._user_repository.set_active(user_id, True)

    def deactivate_staff(self, session: UserSession, user_id: int) -> None:
        """Deactivate a user account without allowing self-lockout."""

        self._require(session, PermissionCode.USERS_MANAGE.value)
        if session.user.id == user_id:
            raise ValidationError("You cannot deactivate your own account")
        self._ensure_user_exists(user_id)
        self._user_repository.set_active(user_id, False)

    def _validate(self, staff_input: StaffInput) -> None:
        if not staff_input.full_name.strip():
            raise ValidationError("Full name is required")
        if not staff_input.username.strip():
            raise ValidationError("Username is required")
        if " " in staff_input.username.strip():
            raise ValidationError("Username must not contain spaces")
        if len(staff_input.password) < 8:
            raise ValidationError("Password must be at least 8 characters")
        role_code = staff_input.role_code.strip().lower()
        if role_code not in {role.value for role in RoleCode}:
            raise ValidationError("Role code is invalid")
        if staff_input.email and "@" not in staff_input.email:
            raise ValidationError("Email address is invalid")

    def _ensure_user_exists(self, user_id: int) -> None:
        if self._user_repository.get_by_id(user_id) is None:
            raise ValidationError("User account not found")

    def _require(self, session: UserSession, permission_code: str) -> None:
        if not session.has_permission(permission_code):
            raise AuthorizationError(f"Missing permission: {permission_code}")
