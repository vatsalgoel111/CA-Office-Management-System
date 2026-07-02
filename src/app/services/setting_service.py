"""
File Purpose: Settings business logic and validation.
Module: app.services.setting_service
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.constants, app.core.exceptions, app.models, app.repositories.
"""

from typing import Dict, List

from app.constants import PermissionCode
from app.core.exceptions import AuthorizationError, ValidationError
from app.models.session import UserSession
from app.models.setting import Setting, SettingInput
from app.repositories.setting_repository import SettingRepository


BOOLEAN_SETTINGS = {"backup.auto_enabled", "notifications.whatsapp_enabled"}
ENUM_SETTINGS: Dict[str, set[str]] = {
    "app.theme": {"light", "dark", "system"},
    "backup.frequency": {"daily", "weekly", "manual"},
}


class SettingService:
    """Business logic for application settings."""

    def __init__(self, setting_repository: SettingRepository) -> None:
        self._setting_repository = setting_repository

    def list_settings(self, session: UserSession) -> List[Setting]:
        """List settings after permission check."""

        self._require(session)
        return self._setting_repository.list_settings()

    def update_setting(self, session: UserSession, setting_input: SettingInput) -> None:
        """Update a setting after validation."""

        self._require(session)
        key = setting_input.key.strip()
        value = setting_input.value.strip()
        self._validate(key, value)
        self._setting_repository.upsert(key, value)

    def get_value(self, key: str, default: str = "") -> str:
        """Return a setting value without requiring a UI session."""

        setting = self._setting_repository.get(key)
        return setting.value if setting is not None else default

    def _validate(self, key: str, value: str) -> None:
        if not key:
            raise ValidationError("Setting key is required")
        if not value:
            raise ValidationError("Setting value is required")
        if key in BOOLEAN_SETTINGS and value.lower() not in {"true", "false"}:
            raise ValidationError("Setting value must be true or false")
        if key in ENUM_SETTINGS and value.lower() not in ENUM_SETTINGS[key]:
            raise ValidationError("Setting value is not allowed")

    def _require(self, session: UserSession) -> None:
        if not session.has_permission(PermissionCode.SETTINGS_MANAGE.value):
            raise AuthorizationError(
                f"Missing permission: {PermissionCode.SETTINGS_MANAGE.value}"
            )
