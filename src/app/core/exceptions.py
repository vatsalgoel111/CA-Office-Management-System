"""
File Purpose: Application-specific exception hierarchy.
Module: app.core.exceptions
Author: CA Office CMS Development Team
Created Date: 2026-07-01
Last Modified: 2026-07-01
Dependencies: Standard library only.
"""


class CAOfficeCMSError(Exception):
    """Base exception for expected application errors."""


class ConfigurationError(CAOfficeCMSError):
    """Raised when application configuration is invalid."""


class StartupError(CAOfficeCMSError):
    """Raised when the application cannot start safely."""


class PathConfigurationError(CAOfficeCMSError):
    """Raised when required runtime paths cannot be prepared."""


class DatabaseError(CAOfficeCMSError):
    """Raised for database adapter or persistence failures."""


class UnsupportedDatabaseProviderError(DatabaseError):
    """Raised when a configured database provider is not implemented."""

