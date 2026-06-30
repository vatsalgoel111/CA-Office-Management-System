"""
File Purpose: Centralized runtime path management.
Module: app.core.paths
Author: CA Office CMS Development Team
Created Date: 2026-07-01
Last Modified: 2026-07-01
Dependencies: dataclasses, pathlib, app.config, app.core.exceptions.
"""

from dataclasses import dataclass
from pathlib import Path

from app.config import AppConfig
from app.core.exceptions import PathConfigurationError


@dataclass(frozen=True)
class AppPaths:
    """Resolved project and runtime paths."""

    project_root: Path
    runtime_root: Path
    config_dir: Path
    data_dir: Path
    backups_dir: Path
    exports_dir: Path
    excel_exports_dir: Path
    pdf_exports_dir: Path
    logs_dir: Path
    database_file: Path
    log_file: Path


def build_paths(config: AppConfig) -> AppPaths:
    """Build all application paths from configuration."""

    runtime_root = config.runtime_root
    data_dir = runtime_root / "data"
    backups_dir = runtime_root / "backups"
    exports_dir = runtime_root / "exports"
    logs_dir = runtime_root / "logs"

    return AppPaths(
        project_root=config.project_root,
        runtime_root=runtime_root,
        config_dir=config.project_root / "config",
        data_dir=data_dir,
        backups_dir=backups_dir,
        exports_dir=exports_dir,
        excel_exports_dir=exports_dir / "excel",
        pdf_exports_dir=exports_dir / "pdf",
        logs_dir=logs_dir,
        database_file=data_dir / config.database_name,
        log_file=logs_dir / config.log_filename,
    )


def ensure_runtime_directories(paths: AppPaths) -> None:
    """Create runtime directories required by the application."""

    directories = (
        paths.runtime_root,
        paths.config_dir,
        paths.data_dir,
        paths.backups_dir,
        paths.exports_dir,
        paths.excel_exports_dir,
        paths.pdf_exports_dir,
        paths.logs_dir,
    )

    try:
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise PathConfigurationError(
            f"Unable to prepare runtime directory: {exc}"
        ) from exc

