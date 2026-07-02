"""
File Purpose: Backup domain models.
Module: app.models.backup
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: dataclasses, pathlib.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BackupResult:
    """Result of a backup operation."""

    file_path: Path
    size_bytes: int
    integrity_ok: bool


@dataclass(frozen=True)
class BackupFile:
    """Backup file metadata for listing."""

    file_path: Path
    size_bytes: int
    created_at: str
