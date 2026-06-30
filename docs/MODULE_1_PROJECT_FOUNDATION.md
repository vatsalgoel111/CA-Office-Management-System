# Module 1: Project Foundation

## Current Step

Step 4: Database

## Purpose

Module 1 creates the technical foundation that every future module depends on.

We are not building user-facing features yet. We are creating the base structure, configuration, logging, database initialization, and testing setup so future modules can be implemented cleanly.

## Why This Module Comes First

Starting with screens before infrastructure creates fragile software. A production desktop app needs predictable paths, logging, database setup, test structure, and clean module boundaries before features are added.

This module prevents these common problems:

- UI files containing SQL.
- Hardcoded database paths.
- Missing logs when production errors occur.
- Unclear folder ownership.
- No safe place for schema changes.
- No repeatable way to run tests.

## Module Scope

This module will create:

- Professional source folder structure.
- Python package layout.
- Application entry point.
- Application startup sequence.
- Central configuration module.
- Runtime path management.
- Central logging setup.
- Basic exception classes.
- Application constants.
- Dependency management files.
- SQLite connection helper.
- Initial database schema file.
- Database initialization script.
- Basic test setup.
- Documentation updates.

## Out of Scope

This module will not implement:

- Login screen.
- User authentication workflow.
- Client management.
- Work allocation.
- Billing.
- Reports.
- WhatsApp sending.
- Installer packaging.

Those belong to later modules.

## Architecture for This Module

The foundation will follow the approved layered architecture:

```text
UI -> Controller -> Service -> Repository -> Database Adapter -> SQLite
```

In Module 1, we only create the structure and shared core utilities needed to support that architecture.

## Planned Folder Structure for Module 1

```text
src/app/
|-- controllers/
|-- services/
|-- repositories/
|-- database/
|   `-- migrations/
|-- models/
|-- ui/
|-- automation/
|-- reports/
|-- core/
`-- utils/
```

Supporting folders:

```text
assets/
config/
exports/
backups/
logs/
tests/
docs/
scripts/
```

## Tooling Verification

Verified on 2026-07-01:

- Python 3.9.13 is installed.
- pip is installed.
- Git 2.49.0 is installed.

No additional software installation is required for Step 1.

## Step Plan

### Step 1: Planning

Create this module plan and define acceptance criteria.

### Step 2: Architecture

Create the scalable `src/app` folder and package structure only.

### Step 3: Core Foundation

Create application entry point, startup sequence, configuration management, path management, logging framework, exception hierarchy, dependency management files, application constants, and minimal core utilities.

Why this comes before database: the database location, logging behavior, and error handling should be defined before database initialization code is written.

### Step 4: Database

Create the initial schema file and database initialization design.

### Step 5: UI Design

Create only a minimal placeholder startup strategy. No real UI feature screens yet.

### Step 6: Implementation

Implement configuration, path management, logging, database connection, and initialization script.

### Step 7: Testing

Add basic tests for path creation, logging setup, and database initialization.

### Step 8: Improvements

Review code quality, docs, and edge cases.

### Step 9: Git Commit

Commit the completed foundation module.

## Foundation Sequence Review

The following components should be completed before the database schema is finalized:

| Component | Before schema? | Reason |
| --- | --- | --- |
| Application entry point (`main.py`) | Yes | Defines how the app starts and where initialization belongs |
| Application startup sequence | Yes | Prevents random initialization code spread across modules |
| Configuration management | Yes | Database paths, environment mode, and logging settings depend on config |
| Environment configuration | Yes, minimal | `.env` is not required immediately, but `.env.example` should document future local overrides |
| Logging framework | Yes | Database initialization failures must be logged from day one |
| Exception hierarchy | Yes | Database errors should use consistent application exceptions |
| Path management | Yes | Database, backups, exports, and logs need centralized paths |
| Dependency management | Yes | Required packages and dev packages must be declared clearly |
| Database connection manager | With database step | It belongs directly beside schema and initialization work |
| Application constants | Yes | Roles, permissions, statuses, and app metadata should be centralized |
| Core utilities | Yes, minimal | Only utilities needed by foundation should be created now |

Decision: add a Core Foundation step before the Database step to reduce future refactoring.

## Acceptance Criteria

Module 1 is complete only when:

- The planned folder structure exists.
- The app can be started from source without crashing.
- Logging creates a log file.
- SQLite database initialization creates required tables.
- Database foreign keys are enabled.
- Basic tests pass.
- Documentation is updated.
- Git commit is created.

## Risks and Controls

| Risk | Control |
| --- | --- |
| Hardcoded developer paths | Use centralized path management |
| UI freezing during future long tasks | Reserve `workers/` for background jobs |
| Database schema drift | Use `schema.sql` and future migrations |
| Missing production diagnostics | Add central logging now |
| Future database migration difficulty | Keep SQLite details behind core database and repositories |

## Current Status

Step 4 is complete after the initial schema, seed data, database initializer, and integrity check flow are created and verified.
