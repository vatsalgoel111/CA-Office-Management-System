"""
File Purpose: Controller for client management UI workflows.
Module: app.controllers.client_controller
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.core.exceptions, app.models, app.services.
"""

from typing import List, Optional

from app.core.exceptions import CAOfficeCMSError
from app.models.client import Client, ClientInput
from app.models.session import UserSession
from app.services.client_service import ClientService


class ClientController:
    """Coordinates client UI actions with service logic."""

    def __init__(self, client_service: ClientService, session: UserSession) -> None:
        self._client_service = client_service
        self._session = session

    def search(self, search_text: str = "") -> List[Client]:
        """Search active clients."""

        return self._client_service.search_clients(self._session, search_text)

    def create(self, client_input: ClientInput) -> Optional[str]:
        """Create a client and return an error message on failure."""

        try:
            self._client_service.create_client(self._session, client_input)
        except CAOfficeCMSError as exc:
            return str(exc)
        return None

    def deactivate(self, client_id: int) -> Optional[str]:
        """Deactivate a client and return an error message on failure."""

        try:
            self._client_service.deactivate_client(self._session, client_id)
        except CAOfficeCMSError as exc:
            return str(exc)
        return None

