# Module 3 Review: Application Shell and Dashboard Routing

Date: 2026-07-02

## What Was Completed

- Module 3 planning and architecture review.
- Application shell coordinator.
- Startup flow now initializes the database before GUI routing.
- Login route registered through `WindowManager`.
- Authenticated shell route registered through `WindowManager`.
- Placeholder dashboard route.
- Permission-aware navigation metadata.
- Shell route tests.

## Files Created

- `docs/MODULE_3_APP_SHELL_DASHBOARD_ROUTING.md`
- `docs/MODULE_3_ARCHITECTURE_REVIEW.md`
- `docs/MODULE_3_REVIEW.md`
- `src/app/app_shell.py`
- `src/app/ui/app_shell.py`
- `src/app/ui/dashboard_placeholder.py`
- `tests/unit/test_app_shell.py`

## Files Modified

- `CHANGELOG.md`
- `TODO.md`
- `src/app/main.py`
- `src/app/ui/__init__.py`

## Architecture Decisions

- Add `ApplicationShell` as the coordinator for startup and routing.
- Keep login view unaware of dashboard internals.
- Keep dashboard as a placeholder only.
- Keep navigation permission-aware through `NavigationItem.required_permission`.

## Why Those Decisions Were Made

- Routing belongs in a coordinator, not inside views.
- Login should authenticate and report success; it should not decide application structure.
- Placeholder dashboard prevents dashboard scope creep.
- Permission-aware navigation prepares future modules without hardcoding role names.

## Risks

- The GUI shell is import-tested but not visually smoke-tested yet.
- First-run admin creation still uses a script, not an in-app setup screen.
- Dashboard metrics are intentionally not implemented yet.

## Suggested Improvements

- Add visual smoke testing once the app can be safely launched in a user-controlled window.
- Add in-app first-run admin setup after basic shell flow is stable.
- Add logout support when the shell grows.

## Testing Performed

- `.venv\Scripts\python.exe -m compileall src scripts tests`
- `.venv\Scripts\python.exe scripts\run_tests.py`
- `.venv\Scripts\python.exe scripts\check_database.py`
- Shell import smoke check.

Result:

- 16 automated tests passed.
- Database integrity check passed.
- Shell imports passed.

## Git Commit Message

Recommended commit message:

```text
feat: add application shell routing
```

## Next Module

Module 4: Dashboard Foundation.

Focus:

- Define dashboard data service boundaries.
- Add real dashboard cards gradually.
- Keep metrics backed by repositories/services, not UI calculations.

