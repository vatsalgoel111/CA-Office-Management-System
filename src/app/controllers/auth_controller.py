"""
File Purpose: Controller for authentication UI workflows.
Module: app.controllers.auth_controller
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.core.exceptions, app.models.session, app.services.auth_service.
"""

from typing import Callable, Optional

from app.core.exceptions import AuthenticationError
from app.models.session import UserSession
from app.services.auth_service import AuthService


class AuthController:
    """Coordinates login UI actions with authentication service logic."""

    def __init__(
        self,
        auth_service: AuthService,
        on_login_success: Optional[Callable[[UserSession], None]] = None,
    ) -> None:
        self._auth_service = auth_service
        self._on_login_success = on_login_success

    def login(self, username: str, password: str) -> Optional[str]:
        """Attempt login and return an error message if it fails."""

        try:
            session = self._auth_service.authenticate(username, password)
        except AuthenticationError as exc:
            return str(exc)

        if self._on_login_success:
            self._on_login_success(session)
        return None

