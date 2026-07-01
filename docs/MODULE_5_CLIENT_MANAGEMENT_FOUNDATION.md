# Module 5: Client Management Foundation

## Current Step

Implementation in progress.

## Purpose

Module 5 adds the foundation for managing CA office clients through clean architecture layers.

## Architecture Review

### Current Design

The project uses:

```text
UI -> Controller -> Service -> Repository -> Database Adapter -> SQLite
```

The `clients` table already exists and supports the required Version 1.0 client master fields.

### Recommended Improvement

Add client-specific model, repository, service, controller, and view. No major architecture change is required.

## Module Scope

- Client model.
- Client repository.
- Client service.
- Client controller.
- Client management view.
- Client search and table display.
- Add client workflow.
- Edit client workflow at service/repository level.
- Soft deactivate workflow.
- Tests for repository and service behavior.

## Out of Scope

- Excel import.
- Client report exports.
- Client portal.
- Document management.
- Advanced duplicate detection.

## Permission Rules

- `clients.view` is required to list/search clients.
- `clients.create` is required to add clients.
- `clients.update` is required to edit clients.
- `clients.deactivate` is required to deactivate clients.

## Acceptance Criteria

- Client logic follows model/repository/service/controller/view layers.
- UI uses reusable components.
- Client search works through repository/service.
- Client creation validates required fields.
- Client deactivation uses soft status update, not hard delete.
- Tests pass.
- Module review is documented.
- Git commit is created.

