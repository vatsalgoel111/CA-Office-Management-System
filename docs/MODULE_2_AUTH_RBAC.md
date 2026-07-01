# Module 2: Authentication and RBAC

## Current Step

Step 4: Implementation in progress.

## Purpose

Module 2 adds secure login and permission-aware access control.

This module must establish the authentication foundation used by every future screen and workflow.

## Why This Module Comes After Foundation

Authentication depends on:

- Database schema.
- User and role tables.
- Configuration.
- Logging.
- Exceptions.
- Reusable UI components.
- Test runner.

Those were created in Module 1, so authentication can now be implemented cleanly.

## Architecture Review

### Current Design

The current architecture is:

```text
UI -> Controller -> Service -> Repository -> Database Adapter -> SQLite
```

RBAC tables already exist:

- `roles`
- `permissions`
- `role_permissions`
- `users`

The UI foundation already supports reusable components and permission-aware navigation primitives.

### Recommended Improvement

Add authentication-specific models, repository, service, controller, and login view using the existing layers.

No global architecture change is required.

### Advantages

- Keeps password logic out of UI.
- Keeps SQL inside repositories.
- Makes permission checks reusable by future modules.
- Keeps future API/cloud migration realistic.

### Disadvantages

- Slightly more code than a simple direct-login script.
- Requires tests across service and repository boundaries.

### Migration Required

No migration is required for the current database. The existing RBAC schema is sufficient for Module 2.

## Module Scope

This module will create:

- User and role models.
- User repository.
- Permission repository or permission query methods.
- Password hashing utility.
- Authentication service.
- Session object.
- Authentication controller.
- Login screen using reusable UI components.
- First-run admin creation helper if no user exists.
- Auth and RBAC tests.

## Out of Scope

This module will not implement:

- Dashboard metrics.
- Client management.
- Staff management screens beyond login identity support.
- Password reset by email.
- Multi-factor authentication.
- Cloud login.

## Security Design

Password hashing will use Python standard library PBKDF2-HMAC-SHA256 with:

- Per-user random salt.
- High iteration count.
- Constant-time password verification.
- Encoded password hash string containing algorithm, iterations, salt, and hash.

Reason: it is secure enough for a local desktop Version 1.0, free, dependency-free, and avoids adding authentication dependencies prematurely.

Future improvement:

- Consider Argon2 or bcrypt if the deployment risk profile increases or if cloud login is introduced.

## Planned Folder Additions

```text
src/app/models/
|-- user.py
`-- session.py

src/app/repositories/
`-- user_repository.py

src/app/services/
`-- auth_service.py

src/app/controllers/
`-- auth_controller.py

src/app/ui/
`-- login_view.py

tests/unit/
|-- test_security.py
`-- test_auth_service.py

tests/integration/
`-- test_user_repository.py
```

## Login Flow

```text
LoginView
|
AuthController.login(username, password)
|
AuthService.authenticate(username, password)
|
UserRepository.get_by_username(username)
|
Password verification
|
Session created
|
Permission list loaded
|
Next view decided by role/permissions
```

## Permission Rules

- UI may hide unavailable navigation items.
- Services must still enforce permissions.
- Permission checks should use permission codes, not hardcoded role names.
- Administrator receives all permissions from seed data.

## Step Plan

### Step 1: Planning and Architecture Review

Create this document and confirm no major architectural change is required.

### Step 2: Database Review

Confirm existing RBAC tables and decide whether first-run admin setup needs schema changes.

### Step 3: UI Design

Design the login screen layout using existing UI components.

### Step 4: Implementation

Implement password hashing, repositories, services, controller, and login view.

### Step 5: Testing

Add unit and integration tests for authentication and permissions.

### Step 6: Improvements

Review security, error handling, and user experience.

### Step 7: Git Commit

Commit the completed authentication module.

## Acceptance Criteria

Module 2 is complete only when:

- Admin user can be created for first run.
- Valid user can log in.
- Invalid credentials are rejected.
- Inactive users are rejected.
- Password hashes are never stored or logged as plaintext.
- Session contains user identity and permissions.
- Login screen uses reusable UI components.
- Tests pass.
- Documentation is updated.
- Git commit is created.

## Implementation Notes

- Password hashing uses `app.core.security`.
- User persistence uses `UserRepository`.
- Login business rules live in `AuthService`.
- Login UI workflow coordination lives in `AuthController`.
- Login screen is built in `LoginView` using reusable UI components.
- First-run administrator creation is supported by `scripts/create_initial_admin.py`.

## Risks and Controls

| Risk | Control |
| --- | --- |
| Weak password storage | PBKDF2-HMAC-SHA256 with per-user salt |
| UI-only permission enforcement | Service-layer permission checks |
| Leaking sensitive data in logs | Never log plaintext passwords |
| First-run setup confusion | Provide clear admin creation helper |
| Future role expansion | Use permission codes, not role name checks |
