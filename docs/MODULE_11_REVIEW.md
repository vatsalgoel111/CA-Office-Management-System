# Module 11 Review: Audit Log Foundation

## What Was Completed

- Added audit log domain models.
- Added audit repository for append-only event recording and recent-entry search.
- Added audit service with validation and `audit.view` read permission.
- Added audit controller.
- Added read-only Audit Log screen and route.
- Added integration tests for audit record/search/permission behavior.

## Files Created

- `src/app/models/audit.py`
- `src/app/repositories/audit_repository.py`
- `src/app/services/audit_service.py`
- `src/app/controllers/audit_controller.py`
- `src/app/ui/audit_view.py`
- `tests/integration/test_audit_service.py`
- `docs/MODULE_11_AUDIT_LOG_FOUNDATION.md`
- `docs/MODULE_11_REVIEW.md`

## Files Modified

- `src/app/ui/app_shell.py`
- `src/app/ui/__init__.py`
- `tests/unit/test_app_shell.py`
- `CHANGELOG.md`
- `TODO.md`

## Architecture Decisions

- Audit logs are append-only through the repository.
- Audit event recording does not require `audit.view`; viewing does.
- System events can use `session=None`.
- Structured old/new values are JSON-encoded in the service.

## Why Those Decisions Were Made

- Audit recording must be available to internal workflows that should not need read permission.
- System events such as backups and automations may not have an active user.
- JSON-encoded values keep the current SQLite schema portable while supporting future detail views.

## Risks

- Existing business services are not yet wired to automatically record every change.
- Audit log tamper-evidence is not implemented yet.
- The viewer has simple search only.

## Suggested Improvements

- Inject audit service into business services and record key create/update/status events.
- Add date/user/entity filters.
- Add tamper-evident hash chain for production hardening.
- Add audit export through the reporting module.

## Testing Performed

- Compile check for `src`, `scripts`, and `tests`.
- Full test suite through `scripts/run_tests.py`.
- Database health check through `scripts/check_database.py`.

## Git Commit Message

`feat: add audit log foundation`

## Next Module

Module 12: Automatic Backup Foundation.
