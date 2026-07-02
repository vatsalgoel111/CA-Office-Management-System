"""
File Purpose: Controller for collection tracking UI workflows.
Module: app.controllers.collection_controller
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.core.exceptions, app.models, app.services.
"""

from typing import List, Optional

from app.core.exceptions import CAOfficeCMSError
from app.models.collection import CollectionInput, CollectionRecord
from app.models.session import UserSession
from app.services.collection_service import CollectionService


class CollectionController:
    """Coordinates collection UI actions with service logic."""

    def __init__(
        self,
        collection_service: CollectionService,
        session: UserSession,
    ) -> None:
        self._collection_service = collection_service
        self._session = session

    def list_collections(self, search_text: str = "") -> List[CollectionRecord]:
        """Return collection records."""

        return self._collection_service.list_collections(self._session, search_text)

    def record(self, collection_input: CollectionInput) -> Optional[str]:
        """Record a collection and return an error message on failure."""

        try:
            self._collection_service.record_collection(self._session, collection_input)
        except CAOfficeCMSError as exc:
            return str(exc)
        return None
