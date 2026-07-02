"""
File Purpose: Controller for settings UI workflows.
Module: app.controllers.setting_controller
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.core.exceptions, app.models, app.services.
"""

from typing import List, Optional

from app.core.exceptions import CAOfficeCMSError
from app.models.session import UserSession
from app.models.setting import Setting, SettingInput
from app.services.setting_service import SettingService


class SettingController:
    """Coordinates settings UI actions with service logic."""

    def __init__(self, setting_service: SettingService, session: UserSession) -> None:
        self._setting_service = setting_service
        self._session = session

    def list_settings(self) -> List[Setting]:
        """Return settings."""

        return self._setting_service.list_settings(self._session)

    def update(self, setting_input: SettingInput) -> Optional[str]:
        """Update a setting and return an error message on failure."""

        try:
            self._setting_service.update_setting(self._session, setting_input)
        except CAOfficeCMSError as exc:
            return str(exc)
        return None
