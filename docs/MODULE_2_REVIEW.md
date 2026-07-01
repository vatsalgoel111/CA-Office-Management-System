# Module 2 Review: Authentication and RBAC

Date: 2026-07-02

## What Was Completed

- Module 2 planning and architecture review.
- Password hashing and verification helper.
- User and session models.
- User repository for authentication and permission lookup.
- Authentication service.
- Authorization permission check helper.
- Authentication controller.
- Login view using reusable UI components.
- First-run administrator creation script.
- Authentication and security tests.

## Files Created

- `docs/MODULE_2_AUTH_RBAC.md`
- `docs/MODULE_2_ARCHITECTURE_REVIEW.md`
- `docs/MODULE_2_REVIEW.md`
- `src/app/core/security.py`
- `src/app/models/user.py`
- `src/app/models/session.py`
- `src/app/repositories/user_repository.py`
- `src/app/services/auth_service.py`
- `src/app/controllers/auth_controller.py`
- `src/app/ui/login_view.py`
- `scripts/create_initial_admin.py`
- `tests/unit/test_security.py`
- `tests/integration/test_auth_service.py`

## Files Modified

- `CHANGELOG.md`
- `TODO.md`
- `docs/DATABASE.md`
- `src/app/core/exceptions.py`
- `src/app/ui/__init__.py`

## Architecture Decisions

- Passwords are hashed with PBKDF2-HMAC-SHA256 using the Python standard library.
- Password hashes store algorithm, iterations, salt, and hash in one encoded string.
- Permission checks are exposed through `AuthService.require_permission`.
- Login UI uses `LoginView` and reusable form/button components.
- User lookup and permission loading stay inside `UserRepository`.

## Why Those Decisions Were Made

- PBKDF2-HMAC-SHA256 avoids extra dependencies while remaining suitable for local Version 1.0 deployment.
- The encoded hash format allows future iteration count changes without breaking old users.
- Service-layer permission checks prevent UI-only security.
- Repository isolation keeps future database migration practical.
- Reusing the UI foundation prevents inconsistent login screen controls.

## Risks

- PBKDF2 is acceptable, but Argon2 or bcrypt may be preferred if the app later becomes cloud-connected.
- The login view is import-tested but not visually tested yet.
- No account lockout policy exists yet.
- No password reset flow exists yet.

## Suggested Improvements

- Add account lockout or login attempt tracking after audit logging is wired into services.
- Add password policy validation before production.
- Visually test login screen once the app shell is launched.
- Consider Argon2 or bcrypt before any cloud or multi-office release.

## Testing Performed

- `.venv\Scripts\python.exe -m compileall src scripts tests`
- `.venv\Scripts\python.exe scripts\run_tests.py`
- `.venv\Scripts\python.exe scripts\check_database.py`
- Auth import smoke check.

Result:

- 14 automated tests passed.
- Database integrity check passed.
- Authentication rejects invalid passwords.
- Initial admin can be created only once.
- Administrator receives expected permissions.

## Git Commit Message

Recommended commit message:

```text
feat: add authentication and RBAC foundation
```

## Next Module

Module 3: Application Shell and Dashboard Routing.

Focus:

- Wire window manager to startup.
- Add authenticated app shell.
- Route login success to a placeholder authenticated area.
- Prepare dashboard module without building full dashboard metrics yet.

