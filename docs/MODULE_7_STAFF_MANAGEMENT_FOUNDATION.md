# Module 7: Staff Management Foundation

## Current Step

Completed.

## Purpose

Module 7 adds staff account management on top of the existing user, role, and permission schema.

## Architecture Review

### Current Design

The project already uses `users`, `roles`, `permissions`, and `role_permissions` for login and RBAC.

### Decision

Staff management reuses the existing user system instead of creating a separate staff table.

## Why

- Staff accounts must be able to log in.
- Work assignment already points to `users`.
- Role-based access should stay centralized.
- Future migration to PostgreSQL/MySQL remains simpler with one normalized account model.

## Module Scope

- Staff input model.
- User repository extensions for listing, lookup, and activation status changes.
- Staff service with validation and `users.manage` permission checks.
- Staff controller for UI workflows.
- Staff management view.
- Staff route in authenticated shell.
- Integration tests for create, list, activate, deactivate, permissions, and validation.

## Out of Scope

- Password reset workflow.
- Granular custom role editor.
- Attendance and leave management.
- Staff performance reporting.

## Acceptance Criteria

- Staff management follows model/repository/service/controller/view layers. Completed.
- Only users with `users.manage` can manage staff accounts. Completed.
- Duplicate usernames are rejected before database insertion. Completed.
- Admin self-deactivation is blocked. Completed.
- Staff UI uses reusable components. Completed.
- Tests pass. Completed.
- Module review is documented. Completed.
- Git commit is created. Pending until final verification.
