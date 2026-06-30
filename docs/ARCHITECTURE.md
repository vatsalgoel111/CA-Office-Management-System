# Architecture

The application will use a layered desktop architecture:

```text
CustomTkinter UI
        |
Controllers / ViewModels
        |
Service Layer
        |
Repository Layer
        |
Database Adapter
        |
SQLite Database
```

## Why This Architecture

Desktop applications become difficult to maintain when button click handlers contain business logic and SQL queries. We will separate responsibilities so each layer can change independently.

This is especially important because Version 1.0 uses SQLite, but future versions may move to PostgreSQL, MySQL, or a server-backed API.

## Layer Responsibilities

### UI Layer

The UI layer contains CustomTkinter windows, frames, widgets, layout, and user-facing messages.

Rules:

- No SQL queries.
- No direct database access.
- No password hashing logic.
- No business workflow decisions beyond basic UI state.
- Calls controllers or view models only.

### Controller / ViewModel Layer

Controllers connect UI events to application use cases.

Responsibilities:

- Convert UI input into service request data.
- Call services.
- Convert service results into UI-friendly data.
- Handle user-facing validation messages.
- Keep screens free from business and database details.

Why this exists: without this layer, desktop UI files usually become large and hard to test. The controller layer lets us test workflows without starting the full GUI.

### Service Layer

Services contain business rules.

Responsibilities:

- Permission checks.
- Workflow rules.
- Validation coordination.
- Audit log coordination.
- Notification queue coordination.
- Backup and report orchestration.

Services should not know CustomTkinter details.

### Repository Layer

Repositories isolate database queries from business logic.

Responsibilities:

- Execute parameterized SQL.
- Map database rows to model objects or dictionaries.
- Keep SQL in one predictable place.
- Avoid leaking SQLite-specific details into services.

### Database Adapter Layer

The database adapter owns connection creation, transactions, foreign key enforcement, and database-specific setup.

For SQLite this includes:

- Enabling foreign keys.
- Setting WAL mode where appropriate.
- Managing transaction boundaries.
- Providing safe connection helpers.

Future PostgreSQL or MySQL migration should mainly affect this layer and repository SQL, not UI or service code.

## Dependency Direction

Dependencies must point inward:

```text
UI -> Controller -> Service -> Repository -> Database Adapter
```

Lower layers must not import higher layers. For example, repositories must never import UI modules.

## Continuous Architecture Review

Before starting every new module, review the existing architecture.

If an improvement is found, document:

- Current design.
- Recommended improvement.
- Advantages.
- Disadvantages.
- Whether migration is required.

Major architectural or technology changes require user approval before implementation.

## Example Flow: Work Assignment

```text
Assign button
|
WorkAllocationView
|
WorkAllocationController.assign_work()
|
WorkService.assign_work()
|
WorkRepository.create()
|
SQLite transaction
|
AuditLogService.record()
|
NotificationService.queue_work_assignment()
```

## Desktop Application Strategy

The application is a single desktop process in Version 1.0. SQLite works well for this model when used carefully.

For staff laptops, the first production design should avoid multiple users writing to the same SQLite file over an unstable network share. That setup can corrupt workflows and create locking problems.

Recommended Version 1.0 deployment:

- One server or main office laptop hosts the primary database.
- Staff use the application on the same machine, through remote desktop, or through a carefully controlled shared-office setup.
- Before true multi-machine concurrent usage, we should introduce either a small local server API or migrate to PostgreSQL/MySQL.

This is a critical commercial design note. SQLite is excellent for local embedded storage, but it is not a replacement for a multi-user database server.

## WhatsApp Integration Architecture

WhatsApp must be isolated behind a notification interface.

```text
Business event
|
NotificationService
|
NotificationQueueRepository
|
NotificationProvider
|
WhatsApp Web automation or future official API
```

Rules:

- Business services only queue notifications.
- Provider code sends notifications.
- Failed sends are stored and retried.
- WhatsApp Web automation is treated as replaceable because it can break if WhatsApp changes its UI.
- Paid APIs are avoided in Version 1.0 unless the user explicitly approves later.

## Error Handling Architecture

- Repositories raise technical exceptions.
- Services catch expected repository failures and convert them into application-level errors.
- Controllers convert application errors into user-friendly messages.
- Unexpected exceptions are logged with context and shown as safe messages.

## Logging Architecture

Logging will be centralized in `app/core/logger.py`.

Log categories:

- Application startup and shutdown.
- Authentication events.
- Database initialization and migration.
- Backup success and failure.
- Report export success and failure.
- Notification send success and failure.
- Unexpected exceptions.

Logs must not store plaintext passwords or sensitive secrets.
