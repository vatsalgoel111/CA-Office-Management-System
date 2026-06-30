"""
File Purpose: Modular application startup orchestration.
Module: app.startup
Author: CA Office CMS Development Team
Created Date: 2026-07-01
Last Modified: 2026-07-01
Dependencies: dataclasses, logging, app.config, app.core, app.database.
"""

from dataclasses import dataclass
import logging

from app.config import AppConfig, load_config
from app.core.exceptions import CAOfficeCMSError, StartupError
from app.core.logger import configure_logging
from app.core.paths import AppPaths, build_paths, ensure_runtime_directories
from app.database.connection import DatabaseConnectionManager, create_connection_manager


@dataclass(frozen=True)
class ApplicationContext:
    """Resolved application dependencies created at startup."""

    config: AppConfig
    paths: AppPaths
    logger: logging.Logger
    database: DatabaseConnectionManager


def initialize_application() -> ApplicationContext:
    """Initialize configuration, paths, logging, and core adapters."""

    try:
        config = load_config()
        paths = build_paths(config)
        ensure_runtime_directories(paths)
        logger = configure_logging(config, paths)
        database = create_connection_manager(config, paths)
        logger.info("Application core foundation initialized")
        return ApplicationContext(
            config=config,
            paths=paths,
            logger=logger,
            database=database,
        )
    except CAOfficeCMSError:
        raise
    except Exception as exc:
        raise StartupError(f"Unexpected startup failure: {exc}") from exc

