"""
File Purpose: Lookup choice models for user-friendly UI selectors.
Module: app.models.lookup
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: dataclasses.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LookupChoice:
    """ID-backed display choice for UI dropdowns."""

    id: int
    label: str

    @property
    def display(self) -> str:
        """Return display text without exposing database ID prominently."""

        return self.label
