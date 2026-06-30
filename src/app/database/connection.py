"""
File Purpose: Database connection manager abstraction.
Module: app.database.connection
Author: CA Office CMS Development Team
Created Date: 2026-07-01
Last Modified: 2026-07-01
Dependencies: abc, contextlib, sqlite3, typing, app.config, app.constants, app.core.
"""

from abc import ABC, abstractmethod
from contextlib import contextmanager
import sqlite3
from typing import Iterator

from app.config import AppConfig
from app.constants import DatabaseProvider
from app.core.exceptions import (
    DatabaseError,
    UnsupportedDatabaseProviderError,
)
from app.core.paths import AppPaths


class DatabaseConnectionManager(ABC):
    """Abstract database connection manager for repository use."""

    @contextmanager
    @abstractmethod
    def connect(self) -> Iterator[sqlite3.Connection]:
        """Yield a database connection."""

    @contextmanager
    @abstractmethod
    def transaction(self) -> Iterator[sqlite3.Connection]:
        """Yield a database connection inside a transaction."""


class SQLiteConnectionManager(DatabaseConnectionManager):
    """SQLite implementation of the database connection manager."""

    def __init__(self, database_file: str) -> None:
        self._database_file = database_file

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self._database_file)
        try:
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA foreign_keys = ON;")
            connection.execute("PRAGMA journal_mode = WAL;")
            yield connection
        except sqlite3.Error as exc:
            raise DatabaseError(f"SQLite connection error: {exc}") from exc
        finally:
            connection.close()

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        with self.connect() as connection:
            try:
                yield connection
                connection.commit()
            except Exception:
                connection.rollback()
                raise


def create_connection_manager(
    config: AppConfig,
    paths: AppPaths,
) -> DatabaseConnectionManager:
    """Create a database connection manager for the configured provider."""

    if config.database_provider == DatabaseProvider.SQLITE:
        return SQLiteConnectionManager(str(paths.database_file))

    raise UnsupportedDatabaseProviderError(
        f"Database provider is not implemented: {config.database_provider.value}"
    )
