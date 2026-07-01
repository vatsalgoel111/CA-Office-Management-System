"""
File Purpose: Authentication and permission business logic.
Module: app.services.auth_service
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: app.constants, app.core, app.models, app.repositories.
"""

from app.constants import RoleCode
from app.core.exceptions import AuthenticationError, AuthorizationError
from app.core.security import hash_password, verify_password
from app.models.session import UserSession
from app.models.user import CreateUserRequest
from app.repositories.user_repository import UserRepository


class AuthService:
    """Authentication and RBAC service."""

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def authenticate(self, username: str, password: str) -> UserSession:
        """Authenticate a user and return a session."""

        normalized_username = username.strip().lower()
        user = self._user_repository.get_by_username(normalized_username)
        if user is None:
            raise AuthenticationError("Invalid username or password")

        if not user.is_active:
            raise AuthenticationError("User account is inactive")

        if not verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid username or password")

        permissions = self._user_repository.get_permissions_for_user(user.id)
        return UserSession(user=user, permissions=permissions)

    def create_initial_admin(
        self,
        full_name: str,
        username: str,
        password: str,
        mobile: str = "",
        email: str = "",
    ) -> int:
        """Create first administrator user when no users exist."""

        if self._user_repository.count_users() > 0:
            raise AuthenticationError("Initial administrator already exists")

        password_hash = hash_password(password)
        return self._user_repository.create_user(
            CreateUserRequest(
                full_name=full_name,
                username=username,
                password_hash=password_hash,
                role_code=RoleCode.ADMINISTRATOR.value,
                mobile=mobile or None,
                email=email or None,
            )
        )

    def require_permission(
        self,
        session: UserSession,
        permission_code: str,
    ) -> None:
        """Raise if a session lacks a required permission."""

        if not session.has_permission(permission_code):
            raise AuthorizationError(f"Missing permission: {permission_code}")

