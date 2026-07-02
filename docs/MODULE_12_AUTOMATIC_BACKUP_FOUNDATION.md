# Module 12: Automatic Backup Foundation

## Current Step

Completed.

## Purpose

Module 12 adds verified local SQLite database backups and backup retention cleanup.

## Architecture Review

### Current Design

The application has centralized runtime paths and a SQLite database file. The backup folder is already part of the managed runtime structure.

### Decision

Use SQLite's native backup API for database backups.

## Why

- Copying a live SQLite file can produce unsafe backups.
- SQLite's backup API is designed for consistent backups while the database may be open.
- Backup location should use centralized runtime paths.

## Module Scope

- Backup models.
- Backup service.
- Backup controller.
- Backup UI route.
- Manual verified backup creation.
- Backup listing.
- Retention cleanup.
- Integration tests for backup creation, verification, retention, and permissions.

## Out of Scope

- Scheduled background backups.
- Cloud backup.
- Encrypted backup archives.
- Restore workflow.

## Acceptance Criteria

- Backup creation uses SQLite backup API. Completed.
- Backup access requires `backup.create`. Completed.
- Created backups pass integrity check. Completed.
- Backup files are written under configured runtime backup path. Completed.
- Retention cleanup is supported. Completed.
- Tests pass. Completed.
- Module review is documented. Completed.
- Git commit is created. Pending until final verification.
