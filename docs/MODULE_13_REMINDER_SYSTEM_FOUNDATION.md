# Module 13: Reminder System Foundation

## Current Step

Completed.

## Purpose

Module 13 adds overdue and upcoming work reminders based on work due dates.

## Architecture Review

### Current Design

Work items already store due dates, status, assignee, and client relationships.

### Decision

Build reminders as a read-only work intelligence module scoped by existing work permissions.

## Why

- Reminder data should be derived from work items instead of duplicated in another table.
- Staff should only see reminders for assigned work.
- Scheduled delivery belongs in the automation/notification module.

## Module Scope

- Reminder models.
- Reminder repository.
- Reminder service.
- Reminder controller.
- Reminder view and route.
- Integration tests for admin scope, staff scope, validation, and permissions.

## Out of Scope

- Scheduled notification delivery.
- Snooze/dismiss reminder state.
- Calendar integration.

## Acceptance Criteria

- Reminders follow model/repository/service/controller/view layers. Completed.
- Admin/manager users with `work.view_all` see all due work. Completed.
- Staff users with `work.view_assigned` see assigned reminders only. Completed.
- Completed/cancelled work is excluded. Completed.
- Tests pass. Completed.
- Module review is documented. Completed.
- Git commit is created. Pending until final verification.
