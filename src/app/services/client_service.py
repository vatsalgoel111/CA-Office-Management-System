"""
File Purpose: Client business logic and permission checks.
Module: app.services.client_service
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.constants, app.core.exceptions, app.models, app.repositories.
"""

from typing import List

from app.constants import PermissionCode
from app.core.exceptions import AuthorizationError, ValidationError
from app.models.client import Client, ClientInput
from app.models.session import UserSession
from app.repositories.client_repository import ClientRepository


class ClientService:
    """Business logic for client management."""

    def __init__(self, client_repository: ClientRepository) -> None:
        self._client_repository = client_repository

    def search_clients(
        self,
        session: UserSession,
        search_text: str = "",
        include_inactive: bool = False,
    ) -> List[Client]:
        """Search clients after permission check."""

        self._require(session, PermissionCode.CLIENTS_VIEW.value)
        return self._client_repository.search(search_text, include_inactive)

    def create_client(self, session: UserSession, client_input: ClientInput) -> int:
        """Create a client after validation and permission check."""

        self._require(session, PermissionCode.CLIENTS_CREATE.value)
        self._validate(client_input)
        return self._client_repository.create(client_input)

    def update_client(
        self,
        session: UserSession,
        client_id: int,
        client_input: ClientInput,
    ) -> None:
        """Update a client after validation and permission check."""

        self._require(session, PermissionCode.CLIENTS_UPDATE.value)
        self._validate(client_input)
        self._client_repository.update(client_id, client_input)

    def deactivate_client(self, session: UserSession, client_id: int) -> None:
        """Soft-deactivate a client after permission check."""

        self._require(session, PermissionCode.CLIENTS_DEACTIVATE.value)
        self._client_repository.deactivate(client_id)

    def _validate(self, client_input: ClientInput) -> None:
        if not client_input.client_name.strip():
            raise ValidationError("Client name is required")
        if client_input.email and "@" not in client_input.email:
            raise ValidationError("Email address is invalid")

    def _require(self, session: UserSession, permission_code: str) -> None:
        if not session.has_permission(permission_code):
            raise AuthorizationError(f"Missing permission: {permission_code}")

