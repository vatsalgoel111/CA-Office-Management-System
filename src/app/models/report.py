"""
File Purpose: Report and export domain models.
Module: app.models.report
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: dataclasses, pathlib, typing.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence, Tuple


@dataclass(frozen=True)
class ReportTable:
    """Tabular report data ready for UI display or export."""

    title: str
    columns: Tuple[str, ...]
    rows: Tuple[Tuple[str, ...], ...]

    @property
    def row_count(self) -> int:
        """Return number of data rows."""

        return len(self.rows)


@dataclass(frozen=True)
class ExportResult:
    """Result of an export operation."""

    file_path: Path
    row_count: int


ReportRows = Sequence[Sequence[str]]
