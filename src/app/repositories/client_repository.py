"""
File Purpose: Client persistence operations.
Module: app.repositories.client_repository
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.database.connection, app.models.client.
"""

from typing import List, Optional, Sequence

from app.database.connection import DatabaseConnectionManager
from app.models.client import Client, ClientInput


class ClientRepository:
    """Repository for client master records."""

    def __init__(self, connection_manager: DatabaseConnectionManager) -> None:
        self._connection_manager = connection_manager

    def create(self, client_input: ClientInput) -> int:
        """Create a client and return the new client ID."""

        with self._connection_manager.transaction() as connection:
            cursor = connection.execute(
                """
                INSERT INTO clients (
                    client_name,
                    business_name,
                    mobile,
                    email,
                    pan,
                    gstin,
                    address,
                    client_type,
                    status,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'active', ?);
                """,
                self._input_values(client_input),
            )
            return int(cursor.lastrowid)

    def update(self, client_id: int, client_input: ClientInput) -> None:
        """Update a client."""

        with self._connection_manager.transaction() as connection:
            connection.execute(
                """
                UPDATE clients
                SET
                    client_name = ?,
                    business_name = ?,
                    mobile = ?,
                    email = ?,
                    pan = ?,
                    gstin = ?,
                    address = ?,
                    client_type = ?,
                    notes = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?;
                """,
                (*self._input_values(client_input), client_id),
            )

    def deactivate(self, client_id: int) -> None:
        """Soft-deactivate a client."""

        with self._connection_manager.transaction() as connection:
            connection.execute(
                """
                UPDATE clients
                SET status = 'inactive', updated_at = CURRENT_TIMESTAMP
                WHERE id = ?;
                """,
                (client_id,),
            )

    def get_by_id(self, client_id: int) -> Optional[Client]:
        """Return a client by ID."""

        with self._connection_manager.connect() as connection:
            row = connection.execute(
                """
                SELECT id, client_name, business_name, mobile, email, pan, gstin,
                       address, client_type, status, notes
                FROM clients
                WHERE id = ?;
                """,
                (client_id,),
            ).fetchone()
        return self._map_client(row) if row is not None else None

    def search(self, search_text: str = "", include_inactive: bool = False) -> List[Client]:
        """Search clients by common office fields."""

        query = """
            SELECT id, client_name, business_name, mobile, email, pan, gstin,
                   address, client_type, status, notes
            FROM clients
            WHERE 1 = 1
        """
        params: List[object] = []
        if not include_inactive:
            query += " AND status = 'active'"

        normalized_search = search_text.strip()
        if normalized_search:
            like_value = f"%{normalized_search}%"
            query += """
                AND (
                    client_name LIKE ?
                    OR business_name LIKE ?
                    OR mobile LIKE ?
                    OR pan LIKE ?
                    OR gstin LIKE ?
                )
            """
            params.extend([like_value] * 5)

        query += " ORDER BY client_name COLLATE NOCASE ASC;"
        with self._connection_manager.connect() as connection:
            rows = connection.execute(query, tuple(params)).fetchall()
        return [self._map_client(row) for row in rows]

    def _input_values(self, client_input: ClientInput) -> Sequence[Optional[str]]:
        pan = self._clean(client_input.pan)
        gstin = self._clean(client_input.gstin)
        return (
            client_input.client_name.strip(),
            self._clean(client_input.business_name),
            self._clean(client_input.mobile),
            self._clean(client_input.email),
            pan.upper() if pan else None,
            gstin.upper() if gstin else None,
            self._clean(client_input.address),
            self._clean(client_input.client_type),
            self._clean(client_input.notes),
        )

    def _clean(self, value: str) -> Optional[str]:
        cleaned = value.strip()
        return cleaned or None

    def _map_client(self, row) -> Client:
        return Client(
            id=int(row["id"]),
            client_name=str(row["client_name"]),
            business_name=row["business_name"],
            mobile=row["mobile"],
            email=row["email"],
            pan=row["pan"],
            gstin=row["gstin"],
            address=row["address"],
            client_type=row["client_type"],
            status=str(row["status"]),
            notes=row["notes"],
        )

