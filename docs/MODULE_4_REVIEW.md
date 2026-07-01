# Module 4 Review: Dashboard Foundation

Date: 2026-07-02

## What Was Completed

- Module 4 planning and architecture review.
- Dashboard summary model.
- Dashboard repository with SQL-backed metrics.
- Dashboard service with permission-aware work scoping.
- Dashboard controller.
- Dashboard view using reusable `InfoCard` components.
- Replaced dashboard placeholder with real dashboard foundation.
- Dashboard service integration tests.

## Files Created

- `docs/MODULE_4_DASHBOARD_FOUNDATION.md`
- `docs/MODULE_4_REVIEW.md`
- `src/app/models/dashboard.py`
- `src/app/repositories/dashboard_repository.py`
- `src/app/services/dashboard_service.py`
- `src/app/controllers/dashboard_controller.py`
- `src/app/ui/dashboard_view.py`
- `tests/integration/test_dashboard_service.py`

## Files Modified

- `src/app/app_shell.py`
- `src/app/ui/app_shell.py`
- `src/app/ui/__init__.py`
- `tests/unit/test_app_shell.py`
- `CHANGELOG.md`
- `TODO.md`

## Files Removed

- `src/app/ui/dashboard_placeholder.py`

## Architecture Decisions

- Dashboard metrics are calculated through repository/service/controller layers.
- The UI renders only resolved summary values.
- Staff work metrics are scoped to assigned work unless the session has `work.view_all`.
- Outstanding money remains integer paise in persistence and is formatted by the dashboard model.

## Why Those Decisions Were Made

- Keeping SQL out of the UI preserves maintainability.
- Permission-aware service logic prevents staff users from seeing global work counts.
- Integer paise avoids rounding errors in accounting summaries.
- Reusing `InfoCard` keeps dashboard styling consistent with the design system.

## Risks

- Dashboard UI is import/test verified, but not visually smoke-tested in a live window.
- Metrics are foundational only; no drill-down screens exist yet.
- Outstanding amount assumes bill status is maintained correctly by future billing workflows.

## Suggested Improvements

- Add visual smoke testing once the desktop window can be reviewed.
- Add dashboard drill-down navigation after client/work modules exist.
- Add collection/billing service tests when billing workflows are implemented.

## Testing Performed

- `.venv\Scripts\python.exe -m compileall src scripts tests`
- `.venv\Scripts\python.exe scripts\run_tests.py`
- `.venv\Scripts\python.exe scripts\check_database.py`

Result:

- 19 automated tests passed.
- Database integrity check passed.
- Dashboard counts are tested for admin and staff sessions.

## Git Commit Message

Recommended commit message:

```text
feat: add dashboard foundation
```

## Next Module

Module 5: Client Management Foundation.

Focus:

- Client model.
- Client repository.
- Client service.
- Client controller.
- Client list/add/edit UI using reusable components.
- Client management tests.

