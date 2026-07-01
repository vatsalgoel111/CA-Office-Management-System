# Project Structure

The project uses a `src/app` package layout. This is a production-friendly Python structure because application imports are explicit and tests do not accidentally import files from the repository root.

Planned structure:

```text
CA Office CMS/
|
|-- src/
|   `-- app/
|       |-- controllers/
|       |-- services/
|       |-- repositories/
|       |-- database/
|       |   `-- migrations/
|       |-- models/
|       |-- ui/
|       |-- automation/
|       |-- reports/
|       |-- core/
|       `-- utils/
|
|-- assets/
|   |-- icons/
|   `-- images/
|
|-- config/
|-- exports/
|   |-- excel/
|   `-- pdf/
|-- backups/
|-- logs/
|-- tests/
|   |-- unit/
|   `-- integration/
|-- docs/
|-- scripts/
|
|-- README.md
|-- CHANGELOG.md
|-- ROADMAP.md
|-- TODO.md
|-- requirements.txt
`-- .gitignore
```

## Why This Structure Scales

The structure separates presentation, workflow coordination, business rules, persistence, infrastructure, automation, reporting, tests, and runtime outputs.

The `src/app` layout also supports Version 2 and Version 3 growth because external interfaces can be added without mixing them into the desktop UI.

## Folder Purpose

### `src/`

Contains production Python source code. Keeping source under `src` avoids accidental imports from the repository root.

### `src/app/`

Main application package.

### `src/app/controllers/`

Connects UI actions to service methods. Controllers prepare input for services and prepare service output for the UI.

### `src/app/services/`

Business rules and use-case logic. Services coordinate validation, permissions, repositories, audit logging, notifications, reports, and backups.

### `src/app/repositories/`

Persistence access. Repositories execute parameterized queries and isolate database details from services.

### `src/app/database/`

Database adapters, schema files, seed files, and migration support. Future PostgreSQL/MySQL migration should mainly affect this folder and repositories.

### `src/app/database/migrations/`

Future schema migration files. This keeps production database upgrades controlled.

### `src/app/models/`

Domain models and data transfer objects.

### `src/app/ui/`

CustomTkinter theme manager, reusable components, navigation framework, window manager, screens, and widgets. UI modules must not contain SQL or business rules.

### `src/app/automation/`

Background or scheduled workflows such as reminders, daily summaries, automatic backup triggers, and WhatsApp notification jobs.

### `src/app/reports/`

Report generation logic for Excel, PDF, and charts.

### `src/app/core/`

Shared infrastructure such as logging, path management, security, exceptions, and database connection helpers.

### `src/app/utils/`

Small reusable helpers such as date utilities, validators, and file helpers.

### `assets/`

Static assets such as icons and images used by the desktop UI and installer.

### `config/`

Non-secret configuration templates and default settings. Secrets must not be committed.

### `exports/`

Generated Excel and PDF report output. Runtime files are ignored by Git.

### `backups/`

Generated database backups. Runtime files are ignored by Git.

### `logs/`

Technical application logs. Runtime log files are ignored by Git.

### `tests/`

Automated tests.

### `tests/unit/`

Fast tests for services, utilities, and isolated logic.

### `tests/integration/`

Tests involving SQLite, repositories, or multiple layers.

### `docs/`

Project documentation.

### `scripts/`

Developer and maintenance scripts such as database initialization, import helpers, and packaging helpers.

## Database Migration Readiness

The structure deliberately separates database concerns:

```text
Services -> Repositories -> Database Adapter
```

Future PostgreSQL/MySQL migration should not require rewriting UI screens or business services. The expected change area is:

- `src/app/database/`
- `src/app/repositories/`
- configuration in `config/`
