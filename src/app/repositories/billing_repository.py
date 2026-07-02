"""
File Purpose: Billing persistence operations.
Module: app.repositories.billing_repository
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.database.connection, app.models.billing.
"""

from typing import List, Optional

from app.database.connection import DatabaseConnectionManager
from app.models.billing import Bill, BillInput


class BillingRepository:
    """Repository for bill records."""

    def __init__(self, connection_manager: DatabaseConnectionManager) -> None:
        self._connection_manager = connection_manager

    def create(self, bill_input: BillInput, amount_paise: int) -> int:
        """Create a bill and return the new bill ID."""

        with self._connection_manager.transaction() as connection:
            cursor = connection.execute(
                """
                INSERT INTO bills (
                    client_id,
                    work_item_id,
                    bill_number,
                    bill_date,
                    amount_paise,
                    status
                )
                VALUES (?, ?, ?, ?, ?, 'unpaid');
                """,
                (
                    bill_input.client_id,
                    bill_input.work_item_id,
                    bill_input.bill_number.strip(),
                    bill_input.bill_date,
                    amount_paise,
                ),
            )
            return int(cursor.lastrowid)

    def list_bills(self, search_text: str = "") -> List[Bill]:
        """List bills with client and optional work details."""

        query = """
            SELECT
                bills.id,
                bills.client_id,
                clients.client_name,
                bills.work_item_id,
                work_items.title AS work_title,
                bills.bill_number,
                bills.bill_date,
                bills.amount_paise,
                bills.status
            FROM bills
            JOIN clients ON clients.id = bills.client_id
            LEFT JOIN work_items ON work_items.id = bills.work_item_id
        """
        params = []
        cleaned_search = search_text.strip().lower()
        if cleaned_search:
            query += """
                WHERE LOWER(bills.bill_number) LIKE ?
                   OR LOWER(clients.client_name) LIKE ?
                   OR LOWER(bills.status) LIKE ?
            """
            search_pattern = f"%{cleaned_search}%"
            params.extend([search_pattern, search_pattern, search_pattern])
        query += " ORDER BY bills.bill_date DESC, bills.id DESC;"

        with self._connection_manager.connect() as connection:
            rows = connection.execute(query, tuple(params)).fetchall()
        return [self._map_bill(row) for row in rows]

    def get_by_id(self, bill_id: int) -> Optional[Bill]:
        """Return a bill by ID."""

        with self._connection_manager.connect() as connection:
            row = connection.execute(
                """
                SELECT
                    bills.id,
                    bills.client_id,
                    clients.client_name,
                    bills.work_item_id,
                    work_items.title AS work_title,
                    bills.bill_number,
                    bills.bill_date,
                    bills.amount_paise,
                    bills.status
                FROM bills
                JOIN clients ON clients.id = bills.client_id
                LEFT JOIN work_items ON work_items.id = bills.work_item_id
                WHERE bills.id = ?;
                """,
                (bill_id,),
            ).fetchone()
        return self._map_bill(row) if row is not None else None

    def bill_number_exists(self, bill_number: str) -> bool:
        """Return whether a bill number already exists."""

        with self._connection_manager.connect() as connection:
            count = connection.execute(
                "SELECT COUNT(*) FROM bills WHERE bill_number = ?;",
                (bill_number.strip(),),
            ).fetchone()[0]
        return int(count) > 0

    def client_exists(self, client_id: int) -> bool:
        """Return whether an active client exists."""

        with self._connection_manager.connect() as connection:
            count = connection.execute(
                "SELECT COUNT(*) FROM clients WHERE id = ? AND status = 'active';",
                (client_id,),
            ).fetchone()[0]
        return int(count) > 0

    def work_item_exists(self, work_item_id: int) -> bool:
        """Return whether a work item exists."""

        with self._connection_manager.connect() as connection:
            count = connection.execute(
                "SELECT COUNT(*) FROM work_items WHERE id = ?;",
                (work_item_id,),
            ).fetchone()[0]
        return int(count) > 0

    def update_status(self, bill_id: int, status: str) -> None:
        """Update bill status."""

        with self._connection_manager.transaction() as connection:
            connection.execute(
                """
                UPDATE bills
                SET status = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?;
                """,
                (status, bill_id),
            )

    def _map_bill(self, row) -> Bill:
        return Bill(
            id=int(row["id"]),
            client_id=int(row["client_id"]),
            client_name=str(row["client_name"]),
            work_item_id=row["work_item_id"],
            work_title=row["work_title"],
            bill_number=str(row["bill_number"]),
            bill_date=str(row["bill_date"]),
            amount_paise=int(row["amount_paise"]),
            status=str(row["status"]),
        )
