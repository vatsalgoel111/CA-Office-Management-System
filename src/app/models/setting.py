"""
File Purpose: Application settings domain models.
Module: app.models.setting
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: dataclasses.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Setting:
    """Application setting record."""

    id: int
    key: str
    value: str
    updated_at: str


@dataclass(frozen=True)
class SettingInput:
    """Input data for updating a setting."""

    key: str
    value: str
