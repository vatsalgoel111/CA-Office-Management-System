"""
File Purpose: Centralized and configurable application logging.
Module: app.core.logger
Author: CA Office CMS Development Team
Created Date: 2026-07-01
Last Modified: 2026-07-01
Dependencies: logging, logging.handlers, typing, app.config, app.core.paths.
"""

import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

from app.config import AppConfig
from app.core.paths import AppPaths


LOGGER_NAME = "ca_office_cms"


def configure_logging(config: AppConfig, paths: AppPaths) -> logging.Logger:
    """Configure and return the central application logger."""

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(config.log_level.value)
    logger.propagate = False
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = RotatingFileHandler(
        paths.log_file,
        maxBytes=1_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(config.log_level.value)
    logger.addHandler(file_handler)

    if config.debug:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(config.log_level.value)
        logger.addHandler(console_handler)

    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a child logger under the application logger."""

    if not name:
        return logging.getLogger(LOGGER_NAME)
    return logging.getLogger(f"{LOGGER_NAME}.{name}")
