"""
File Purpose: User and permission persistence operations.
Module: app.repositories.user_repository
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.database.connection, app.models.user.
"""

from typing import FrozenSet, List, Optional

from app.database.connection import DatabaseConnectionManager
from app.models.user import CreateUserRequest, UpdateUserRequest, User


class UserRepository:
    """Repository for users, roles, and permissions."""

    def __init__(self, connection_manager: DatabaseConnectionManager) -> None:
        self._connection_manager = connection_manager

    def count_users(self) -> int:
        """Return total number of users."""

        with self._connection_manager.connect() as connection:
            return int(connection.execute("SELECT COUNT(*) FROM users;").fetchone()[0])

    def get_by_username(self, username: str) -> Optional[User]:
        """Return a user by username."""

        with self._connection_manager.connect() as connection:
            row = connection.execute(
                """
                SELECT
                    users.id,
                    users.full_name,
                    users.username,
                    users.password_hash,
                    users.role_id,
                    roles.code AS role_code,
                    roles.name AS role_name,
                    users.mobile,
                    users.email,
                    users.is_active
                FROM users
                JOIN roles ON roles.id = users.role_id
                WHERE users.username = ?;
                """,
                (username.strip().lower(),),
            ).fetchone()

        if row is None:
            return None
        return self._map_user(row)

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Return a user by ID."""

        with self._connection_manager.connect() as connection:
            row = connection.execute(
                """
                SELECT
                    users.id,
                    users.full_name,
                    users.username,
                    users.password_hash,
                    users.role_id,
                    roles.code AS role_code,
                    roles.name AS role_name,
                    users.mobile,
                    users.email,
                    users.is_active
                FROM users
                JOIN roles ON roles.id = users.role_id
                WHERE users.id = ?;
                """,
                (user_id,),
            ).fetchone()

        if row is None:
            return None
        return self._map_user(row)

    def list_users(
        self,
        search_text: str = "",
        include_inactive: bool = True,
    ) -> List[User]:
        """List users for staff management."""

        query = """
            SELECT
                users.id,
                users.full_name,
                users.username,
                users.password_hash,
                users.role_id,
                roles.code AS role_code,
                roles.name AS role_name,
                users.mobile,
                users.email,
                users.is_active
            FROM users
            JOIN roles ON roles.id = users.role_id
        """
        params = []
        clauses = []
        cleaned_search = search_text.strip().lower()
        if cleaned_search:
            clauses.append(
                """
                (
                    LOWER(users.full_name) LIKE ?
                    OR LOWER(users.username) LIKE ?
                    OR LOWER(roles.name) LIKE ?
                    OR users.mobile LIKE ?
                    OR LOWER(users.email) LIKE ?
                )
                """
            )
            search_pattern = f"%{cleaned_search}%"
            params.extend([search_pattern] * 5)
        if not include_inactive:
            clauses.append("users.is_active = 1")
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY users.is_active DESC, users.full_name ASC;"

        with self._connection_manager.connect() as connection:
            rows = connection.execute(query, tuple(params)).fetchall()
        return [self._map_user(row) for row in rows]

    def create_user(self, request: CreateUserRequest) -> int:
        """Create a user and return the new user ID."""

        with self._connection_manager.transaction() as connection:
            role_row = connection.execute(
                "SELECT id FROM roles WHERE code = ?;",
                (request.role_code,),
            ).fetchone()
            if role_row is None:
                raise ValueError(f"Unknown role code: {request.role_code}")

            cursor = connection.execute(
                """
                INSERT INTO users (
                    full_name,
                    username,
                    password_hash,
                    role_id,
                    mobile,
                    email,
                    is_active
                )
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    request.full_name.strip(),
                    request.username.strip().lower(),
                    request.password_hash,
                    int(role_row["id"]),
                    request.mobile,
                    request.email,
                    1 if request.is_active else 0,
                ),
            )
            return int(cursor.lastrowid)

    def update_user(self, user_id: int, request: UpdateUserRequest) -> None:
        """Update user profile and role."""

        with self._connection_manager.transaction() as connection:
            role_row = connection.execute(
                "SELECT id FROM roles WHERE code = ?;",
                (request.role_code,),
            ).fetchone()
            if role_row is None:
                raise ValueError(f"Unknown role code: {request.role_code}")

            connection.execute(
                """
                UPDATE users
                SET full_name = ?,
                    role_id = ?,
                    mobile = ?,
                    email = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?;
                """,
                (
                    request.full_name.strip(),
                    int(role_row["id"]),
                    request.mobile,
                    request.email,
                    user_id,
                ),
            )

    def set_active(self, user_id: int, is_active: bool) -> None:
        """Activate or deactivate a user."""

        with self._connection_manager.transaction() as connection:
            connection.execute(
                """
                UPDATE users
                SET is_active = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?;
                """,
                (1 if is_active else 0, user_id),
            )

    def get_permissions_for_user(self, user_id: int) -> FrozenSet[str]:
        """Return permission codes assigned to a user through their role."""

        with self._connection_manager.connect() as connection:
            rows = connection.execute(
                """
                SELECT permissions.code
                FROM users
                JOIN role_permissions ON role_permissions.role_id = users.role_id
                JOIN permissions ON permissions.id = role_permissions.permission_id
                WHERE users.id = ?;
                """,
                (user_id,),
            ).fetchall()
        return frozenset(str(row["code"]) for row in rows)

    def _map_user(self, row) -> User:
        return User(
            id=int(row["id"]),
            full_name=str(row["full_name"]),
            username=str(row["username"]),
            password_hash=str(row["password_hash"]),
            role_id=int(row["role_id"]),
            role_code=str(row["role_code"]),
            role_name=str(row["role_name"]),
            mobile=row["mobile"],
            email=row["email"],
            is_active=bool(row["is_active"]),
        )
