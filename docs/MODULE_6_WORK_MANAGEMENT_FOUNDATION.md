# Module 6: Work Management Foundation

## Current Step

Completed.

## Purpose

Module 6 adds the foundation for assigning, viewing, and updating office work items.

## Architecture Review

### Current Design

The project uses:

```text
UI -> Controller -> Service -> Repository -> Database Adapter -> SQLite
```

The `work_items` and `remarks` tables already exist.

### Recommended Improvement

Add work-specific model, repository, service, controller, and view.

No major architecture change is required.

## Module Scope

- Work item model.
- Work assignment input model.
- Work repository.
- Work service with permission checks.
- Work controller.
- Work list and basic assignment view.
- Status update workflow.
- Remark storage workflow.
- Tests for assignment, scoped listing, and status updates.

## Out of Scope

- WhatsApp notifications.
- Calendar reminders.
- Advanced staff management.
- File/document attachments.
- Full work type configuration.

## Permission Rules

- `work.assign` is required to assign work.
- `work.view_all` allows viewing all work.
- `work.view_assigned` allows viewing assigned work.
- `work.update_status` allows updating status for visible work.

## Acceptance Criteria

- Work logic follows model/repository/service/controller/view layers. Completed.
- Staff users only see assigned work unless granted `work.view_all`. Completed.
- Status update validates supported statuses. Completed.
- Remarks are stored in the `remarks` table. Completed.
- UI uses reusable components. Completed.
- Tests pass. Completed.
- Module review is documented. Completed.
- Git commit is created. Pending until final verification.
