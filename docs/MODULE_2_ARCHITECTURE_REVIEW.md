# Module 2 Architecture Review

Date: 2026-07-02

## Current Design

The project currently uses:

```text
UI -> Controller -> Service -> Repository -> Database Adapter -> SQLite
```

The database already contains RBAC tables. The UI foundation already contains reusable components, a window manager, and permission-aware navigation primitives.

## Recommended Improvement

Add authentication-specific layers inside the existing architecture:

- `AuthController`
- `AuthService`
- `UserRepository`
- `User` and `Session` models
- `LoginView`
- Password hashing helpers

## Advantages

- Keeps authentication testable.
- Avoids SQL in UI.
- Avoids password logic in controllers.
- Makes future permissions reusable across modules.
- Supports future migration to API/server authentication.

## Disadvantages

- More initial files than a quick login script.
- Requires disciplined tests and service boundaries.

## Migration Required

No database migration is required before Module 2 implementation.

One documentation correction was required: `roles.code` exists in `schema.sql`, so `docs/DATABASE.md` must list it.

## Decision

Proceed with the existing architecture. No major architectural or technology change is required.

