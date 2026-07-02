"""
File Purpose: Collection persistence operations.
Module: app.repositories.collection_repository
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.database.connection, app.models.collection.
"""

from typing import List, Optional, Tuple

from app.database.connection import DatabaseConnectionManager
from app.models.collection import CollectionInput, CollectionRecord


class CollectionRepository:
    """Repository for payment collections."""

    def __init__(self, connection_manager: DatabaseConnectionManager) -> None:
        self._connection_manager = connection_manager

    def list_collections(self, search_text: str = "") -> List[CollectionRecord]:
        """List collections with bill and client details."""

        query = """
            SELECT
                collections.id,
                collections.bill_id,
                bills.bill_number,
                clients.client_name,
                collections.received_amount_paise,
                collections.received_date,
                collections.payment_mode,
                collections.notes
            FROM collections
            JOIN bills ON bills.id = collections.bill_id
            JOIN clients ON clients.id = bills.client_id
        """
        params = []
        cleaned_search = search_text.strip().lower()
        if cleaned_search:
            query += """
                WHERE LOWER(bills.bill_number) LIKE ?
                   OR LOWER(clients.client_name) LIKE ?
                   OR LOWER(collections.payment_mode) LIKE ?
            """
            search_pattern = f"%{cleaned_search}%"
            params.extend([search_pattern, search_pattern, search_pattern])
        query += " ORDER BY collections.received_date DESC, collections.id DESC;"

        with self._connection_manager.connect() as connection:
            rows = connection.execute(query, tuple(params)).fetchall()
        return [self._map_collection(row) for row in rows]

    def get_bill_financials(self, bill_id: int) -> Optional[Tuple[int, str]]:
        """Return bill amount and status."""

        with self._connection_manager.connect() as connection:
            row = connection.execute(
                "SELECT amount_paise, status FROM bills WHERE id = ?;",
                (bill_id,),
            ).fetchone()
        if row is None:
            return None
        return int(row["amount_paise"]), str(row["status"])

    def get_received_total_paise(self, bill_id: int) -> int:
        """Return total amount received against a bill."""

        with self._connection_manager.connect() as connection:
            value = connection.execute(
                """
                SELECT COALESCE(SUM(received_amount_paise), 0)
                FROM collections
                WHERE bill_id = ?;
                """,
                (bill_id,),
            ).fetchone()[0]
        return int(value or 0)

    def create_and_update_bill_status(
        self,
        collection_input: CollectionInput,
        amount_paise: int,
        bill_amount_paise: int,
    ) -> int:
        """Create a collection and recalculate bill status in one transaction."""

        with self._connection_manager.transaction() as connection:
            cursor = connection.execute(
                """
                INSERT INTO collections (
                    bill_id,
                    received_amount_paise,
                    received_date,
                    payment_mode,
                    notes
                )
                VALUES (?, ?, ?, ?, ?);
                """,
                (
                    collection_input.bill_id,
                    amount_paise,
                    collection_input.received_date,
                    collection_input.payment_mode.strip().lower(),
                    collection_input.notes.strip() or None,
                ),
            )
            total_received = connection.execute(
                """
                SELECT COALESCE(SUM(received_amount_paise), 0)
                FROM collections
                WHERE bill_id = ?;
                """,
                (collection_input.bill_id,),
            ).fetchone()[0]
            new_status = "paid" if int(total_received) >= bill_amount_paise else "partial"
            connection.execute(
                """
                UPDATE bills
                SET status = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?;
                """,
                (new_status, collection_input.bill_id),
            )
            return int(cursor.lastrowid)

    def _map_collection(self, row) -> CollectionRecord:
        return CollectionRecord(
            id=int(row["id"]),
            bill_id=int(row["bill_id"]),
            bill_number=str(row["bill_number"]),
            client_name=str(row["client_name"]),
            received_amount_paise=int(row["received_amount_paise"]),
            received_date=str(row["received_date"]),
            payment_mode=str(row["payment_mode"]),
            notes=row["notes"] or "",
        )
