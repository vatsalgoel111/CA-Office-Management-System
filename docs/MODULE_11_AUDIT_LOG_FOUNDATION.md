# Module 11: Audit Log Foundation

## Current Step

Completed.

## Purpose

Module 11 adds a central append-only audit log foundation and read-only audit viewer.

## Architecture Review

### Current Design

The initial schema already includes `audit_logs`, but no repository, service, or UI existed.

### Decision

Build audit logging as a standalone foundation first, then wire detailed business actions across services in a later hardening pass.

## Why

- A central audit service prevents each module from inventing its own log format.
- System-generated events, such as backups, need to be recordable without a user session.
- Read access must be restricted through `audit.view`.

## Module Scope

- Audit log models.
- Audit repository.
- Audit service with append and read permissions.
- Audit controller.
- Audit viewer route.
- Tests for recording, searching, permission checks, and validation.

## Out of Scope

- Automatic audit hooks in every existing service.
- Audit log export.
- Advanced date/user/entity filters.
- Tamper-evident hashing.

## Acceptance Criteria

- Audit follows model/repository/service/controller/view layers. Completed.
- Events can be recorded with or without a user session. Completed.
- Viewing audit logs requires `audit.view`. Completed.
- Audit viewer is read-only. Completed.
- Tests pass. Completed.
- Module review is documented. Completed.
- Git commit is created. Pending until final verification.
