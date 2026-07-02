"""
File Purpose: Report business logic and CSV export operations.
Module: app.services.report_service
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: csv, datetime, typing, app.constants, app.core, app.models, app.repositories.
"""

import csv
from datetime import datetime
from pathlib import Path
from typing import Dict

from app.constants import PermissionCode
from app.core.exceptions import AuthorizationError, ValidationError
from app.core.paths import AppPaths
from app.models.report import ExportResult, ReportTable
from app.models.session import UserSession
from app.repositories.report_repository import ReportRepository


REPORT_KEYS = {
    "client_summary": "Client Summary",
    "work_status_summary": "Work Status Summary",
    "outstanding_bills": "Outstanding Bills",
    "collection_summary": "Collection Summary",
}


class ReportService:
    """Business logic for reports and CSV exports."""

    def __init__(self, report_repository: ReportRepository, paths: AppPaths) -> None:
        self._report_repository = report_repository
        self._paths = paths

    def available_reports(self) -> Dict[str, str]:
        """Return supported report keys and labels."""

        return dict(REPORT_KEYS)

    def build_report(self, session: UserSession, report_key: str) -> ReportTable:
        """Build a report table after permission check."""

        self._require(session)
        normalized_key = report_key.strip().lower()
        if normalized_key == "client_summary":
            return self._report_repository.client_summary()
        if normalized_key == "work_status_summary":
            return self._report_repository.work_status_summary()
        if normalized_key == "outstanding_bills":
            return self._report_repository.outstanding_bills()
        if normalized_key == "collection_summary":
            return self._report_repository.collection_summary()
        raise ValidationError("Unknown report")

    def export_csv(self, session: UserSession, report_key: str) -> ExportResult:
        """Export a report to CSV."""

        report = self.build_report(session, report_key)
        export_dir = self._paths.exports_dir / "csv"
        export_dir.mkdir(parents=True, exist_ok=True)
        file_path = export_dir / self._build_filename(report_key)
        with file_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(report.columns)
            writer.writerows(report.rows)
        return ExportResult(file_path=file_path, row_count=report.row_count)

    def _build_filename(self, report_key: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_key = report_key.strip().lower().replace(" ", "_")
        return f"{safe_key}_{timestamp}.csv"

    def _require(self, session: UserSession) -> None:
        if not session.has_permission(PermissionCode.REPORTS_VIEW.value):
            raise AuthorizationError(
                f"Missing permission: {PermissionCode.REPORTS_VIEW.value}"
            )
