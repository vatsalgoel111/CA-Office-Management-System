"""
File Purpose: Report data query operations.
Module: app.repositories.report_repository
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: app.database.connection, app.models.report.
"""

from app.database.connection import DatabaseConnectionManager
from app.models.report import ReportTable


class ReportRepository:
    """Repository for read-only report queries."""

    def __init__(self, connection_manager: DatabaseConnectionManager) -> None:
        self._connection_manager = connection_manager

    def client_summary(self) -> ReportTable:
        """Return client summary grouped by status."""

        with self._connection_manager.connect() as connection:
            rows = connection.execute(
                """
                SELECT status, COUNT(*) AS client_count
                FROM clients
                GROUP BY status
                ORDER BY status;
                """
            ).fetchall()
        return ReportTable(
            title="Client Summary",
            columns=("Status", "Clients"),
            rows=tuple((str(row["status"]).title(), str(row["client_count"])) for row in rows),
        )

    def work_status_summary(self) -> ReportTable:
        """Return work count grouped by status."""

        with self._connection_manager.connect() as connection:
            rows = connection.execute(
                """
                SELECT status, COUNT(*) AS work_count
                FROM work_items
                GROUP BY status
                ORDER BY status;
                """
            ).fetchall()
        return ReportTable(
            title="Work Status Summary",
            columns=("Status", "Work Items"),
            rows=tuple(
                (str(row["status"]).replace("_", " ").title(), str(row["work_count"]))
                for row in rows
            ),
        )

    def outstanding_bills(self) -> ReportTable:
        """Return bill-wise outstanding amount report."""

        with self._connection_manager.connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    bills.bill_number,
                    clients.client_name,
                    bills.bill_date,
                    bills.amount_paise,
                    COALESCE(collection_totals.received_amount_paise, 0)
                        AS received_amount_paise,
                    bills.amount_paise
                        - COALESCE(collection_totals.received_amount_paise, 0)
                        AS outstanding_amount_paise,
                    bills.status
                FROM bills
                JOIN clients ON clients.id = bills.client_id
                LEFT JOIN (
                    SELECT bill_id, SUM(received_amount_paise) AS received_amount_paise
                    FROM collections
                    GROUP BY bill_id
                ) AS collection_totals ON collection_totals.bill_id = bills.id
                WHERE bills.status IN ('unpaid', 'partial')
                ORDER BY bills.bill_date ASC, bills.id ASC;
                """
            ).fetchall()
        return ReportTable(
            title="Outstanding Bills",
            columns=(
                "Bill No",
                "Client",
                "Bill Date",
                "Bill Amount",
                "Received",
                "Outstanding",
                "Status",
            ),
            rows=tuple(
                (
                    str(row["bill_number"]),
                    str(row["client_name"]),
                    str(row["bill_date"]),
                    self._format_rupees(int(row["amount_paise"])),
                    self._format_rupees(int(row["received_amount_paise"])),
                    self._format_rupees(int(row["outstanding_amount_paise"])),
                    str(row["status"]).title(),
                )
                for row in rows
            ),
        )

    def collection_summary(self) -> ReportTable:
        """Return collection totals grouped by payment mode."""

        with self._connection_manager.connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    payment_mode,
                    COUNT(*) AS collection_count,
                    SUM(received_amount_paise) AS received_amount_paise
                FROM collections
                GROUP BY payment_mode
                ORDER BY payment_mode;
                """
            ).fetchall()
        return ReportTable(
            title="Collection Summary",
            columns=("Payment Mode", "Collections", "Received"),
            rows=tuple(
                (
                    str(row["payment_mode"]).title(),
                    str(row["collection_count"]),
                    self._format_rupees(int(row["received_amount_paise"] or 0)),
                )
                for row in rows
            ),
        )

    def _format_rupees(self, amount_paise: int) -> str:
        return f"Rs. {amount_paise / 100:,.2f}"
