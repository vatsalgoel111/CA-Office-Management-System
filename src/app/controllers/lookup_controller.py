"""
File Purpose: Controller for shared UI lookup choices.
Module: app.controllers.lookup_controller
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.models.lookup, app.repositories.lookup_repository.
"""

from typing import List

from app.models.lookup import LookupChoice
from app.repositories.lookup_repository import LookupRepository


class LookupController:
    """Provides lookup data for UI selectors."""

    def __init__(self, lookup_repository: LookupRepository) -> None:
        self._lookup_repository = lookup_repository

    def active_clients(self) -> List[LookupChoice]:
        """Return active client choices."""

        return self._lookup_repository.active_clients()

    def active_users(self) -> List[LookupChoice]:
        """Return active user choices."""

        return self._lookup_repository.active_users()

    def work_items(self) -> List[LookupChoice]:
        """Return open work item choices."""

        return self._lookup_repository.work_items()

    def open_bills(self) -> List[LookupChoice]:
        """Return open bill choices."""

        return self._lookup_repository.open_bills()
