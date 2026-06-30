"""
File Purpose: Central application constants used across the project.
Module: app.constants
Author: CA Office CMS Development Team
Created Date: 2026-07-01
Last Modified: 2026-07-01
Dependencies: Standard library only.
"""

from enum import Enum


APP_NAME = "CA Office Management System"
APP_VERSION = "0.1.0-foundation"
APP_AUTHOR = "CA Office CMS Development Team"


class Environment(str, Enum):
    """Supported runtime environments."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class DatabaseProvider(str, Enum):
    """Supported database provider names."""

    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"


class LogLevel(str, Enum):
    """Supported logging levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class RoleCode(str, Enum):
    """Built-in role codes."""

    ADMINISTRATOR = "administrator"
    MANAGER = "manager"
    STAFF = "staff"
    ACCOUNTANT = "accountant"
    READ_ONLY = "read_only"


class PermissionCode(str, Enum):
    """Initial permission codes for RBAC."""

    USERS_MANAGE = "users.manage"
    CLIENTS_VIEW = "clients.view"
    CLIENTS_CREATE = "clients.create"
    CLIENTS_UPDATE = "clients.update"
    CLIENTS_DEACTIVATE = "clients.deactivate"
    WORK_VIEW_ALL = "work.view_all"
    WORK_VIEW_ASSIGNED = "work.view_assigned"
    WORK_ASSIGN = "work.assign"
    WORK_UPDATE_STATUS = "work.update_status"
    BILLING_MANAGE = "billing.manage"
    COLLECTIONS_MANAGE = "collections.manage"
    REPORTS_VIEW = "reports.view"
    SETTINGS_MANAGE = "settings.manage"
    AUDIT_VIEW = "audit.view"
    BACKUP_CREATE = "backup.create"


DEFAULT_DATABASE_FILENAME = "ca_office_cms.sqlite3"
DEFAULT_LOG_FILENAME = "app.log"

