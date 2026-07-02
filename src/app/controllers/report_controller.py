"""
File Purpose: Controller for report UI workflows.
Module: app.controllers.report_controller
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.core.exceptions, app.models, app.services.
"""

from typing import Dict, Optional, Tuple

from app.core.exceptions import CAOfficeCMSError
from app.models.report import ExportResult, ReportTable
from app.models.session import UserSession
from app.services.report_service import ReportService


class ReportController:
    """Coordinates report UI actions with service logic."""

    def __init__(self, report_service: ReportService, session: UserSession) -> None:
        self._report_service = report_service
        self._session = session

    def available_reports(self) -> Dict[str, str]:
        """Return report key-label mapping."""

        return self._report_service.available_reports()

    def build_report(self, report_key: str) -> Tuple[Optional[ReportTable], Optional[str]]:
        """Build a report and return an error message on failure."""

        try:
            return self._report_service.build_report(self._session, report_key), None
        except CAOfficeCMSError as exc:
            return None, str(exc)

    def export_csv(self, report_key: str) -> Tuple[Optional[ExportResult], Optional[str]]:
        """Export a report and return an error message on failure."""

        try:
            return self._report_service.export_csv(self._session, report_key), None
        except CAOfficeCMSError as exc:
            return None, str(exc)
