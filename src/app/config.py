"""
File Purpose: Environment-aware application configuration.
Module: app.config
Author: CA Office CMS Development Team
Created Date: 2026-07-01
Last Modified: 2026-07-01
Dependencies: os, dataclasses, pathlib, typing, app.constants.
"""

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Optional

from app.constants import (
    DEFAULT_DATABASE_FILENAME,
    DEFAULT_LOG_FILENAME,
    DatabaseProvider,
    Environment,
    LogLevel,
)


@dataclass(frozen=True)
class AppConfig:
    """Resolved application configuration."""

    environment: Environment
    debug: bool
    database_provider: DatabaseProvider
    database_name: str
    log_level: LogLevel
    log_filename: str
    project_root: Path
    runtime_root: Path
    database_url: Optional[str] = None


def _read_environment(value: Optional[str]) -> Environment:
    if not value:
        return Environment.DEVELOPMENT
    normalized = value.strip().lower()
    for environment in Environment:
        if environment.value == normalized:
            return environment
    return Environment.DEVELOPMENT


def _read_database_provider(value: Optional[str]) -> DatabaseProvider:
    if not value:
        return DatabaseProvider.SQLITE
    normalized = value.strip().lower()
    for provider in DatabaseProvider:
        if provider.value == normalized:
            return provider
    return DatabaseProvider.SQLITE


def _read_log_level(value: Optional[str], environment: Environment) -> LogLevel:
    if value:
        normalized = value.strip().upper()
        for log_level in LogLevel:
            if log_level.value == normalized:
                return log_level
    if environment == Environment.PRODUCTION:
        return LogLevel.INFO
    return LogLevel.DEBUG


def _read_bool(value: Optional[str], default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def load_config(project_root: Optional[Path] = None) -> AppConfig:
    """Load configuration from environment variables with safe defaults."""

    resolved_project_root = (
        project_root.resolve()
        if project_root is not None
        else Path(__file__).resolve().parents[2]
    )
    environment = _read_environment(os.getenv("CA_CMS_ENV"))
    runtime_root = Path(
        os.getenv("CA_CMS_RUNTIME_ROOT", str(resolved_project_root))
    ).resolve()

    return AppConfig(
        environment=environment,
        debug=_read_bool(
            os.getenv("CA_CMS_DEBUG"),
            default=environment != Environment.PRODUCTION,
        ),
        database_provider=_read_database_provider(os.getenv("CA_CMS_DB_PROVIDER")),
        database_name=os.getenv("CA_CMS_DB_NAME", DEFAULT_DATABASE_FILENAME),
        database_url=os.getenv("CA_CMS_DATABASE_URL"),
        log_level=_read_log_level(os.getenv("CA_CMS_LOG_LEVEL"), environment),
        log_filename=os.getenv("CA_CMS_LOG_FILENAME", DEFAULT_LOG_FILENAME),
        project_root=resolved_project_root,
        runtime_root=runtime_root,
    )
