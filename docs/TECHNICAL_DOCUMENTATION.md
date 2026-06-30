# Technical Documentation

## Architecture Summary

The application uses a layered desktop architecture:

```text
UI -> Controller -> Service -> Repository -> Database Adapter -> SQLite
```

## Key Technical Decisions

### SQLite Instead of Excel

SQLite provides structured data, reliable querying, indexes, relationships, and transaction support. Excel remains useful for import and export, but it is not suitable as the primary database for a production workflow system.

### CustomTkinter for UI

CustomTkinter provides a modern Python desktop UI while remaining free and open source.

### Controller Layer

Controllers keep UI files clean by translating UI events into service calls. This makes workflows easier to test without launching the GUI.

### Repository Pattern

Repositories isolate SQL from business logic and UI code.

### Service Layer

Services contain business rules such as permission checks, validation coordination, audit logging, backup orchestration, and notification triggers.

### Database Adapter

The database adapter owns connection handling, transaction helpers, foreign key setup, and database-specific behavior. This keeps future database migration more realistic.

### Core Foundation Before Database Schema

The application entry point, startup sequence, configuration, path management, logging, exception hierarchy, constants, and dependency files should exist before database schema implementation.

Reason: database initialization needs stable paths, predictable logging, and consistent error handling. Creating the database first would increase the chance of hardcoded paths and scattered startup logic.

### RBAC Foundation

Version 1.0 may expose only Administrator and Staff, but the database and service design should support future roles and permissions. This prevents a later redesign when Manager, Accountant, or Read Only roles are added.

## Logging Strategy

Technical logs are stored separately from business audit logs.

Technical logs answer:

- Did the application start correctly?
- Did a backup fail?
- Did a report export fail?
- Did a notification provider fail?
- Was there an unexpected exception?

Audit logs answer:

- Who created or changed a business record?
- What entity was affected?
- When did the action happen?
- What changed?

## Error Handling Strategy

Expected business errors should be shown clearly to the user. Unexpected technical errors should be logged and converted into safe user messages.

Examples:

- Invalid login: show "Invalid username or password."
- Missing required client name: show field validation message.
- Database locked: show retry guidance and log technical details.
- Backup failure: show backup failure message and log exact exception.

## Backup and Recovery Strategy

Backups must be treated as a feature, not an afterthought.

Minimum behavior:

- Automatic daily backup.
- Manual backup.
- Integrity check after backup.
- Recovery documentation.
- Clear logging.

## WhatsApp Strategy

WhatsApp integration is an infrastructure provider, not business logic.

Services create notification requests. A notification worker/provider sends them. This allows WhatsApp Web automation to be replaced later with an official API or another provider.

## Future Technical Notes

This document will be expanded as modules are implemented.
