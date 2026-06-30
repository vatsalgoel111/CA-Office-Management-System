# Non-Functional Requirements

## Reliability

- SQLite must be the permanent database for Version 1.0.
- Important database writes must use transactions.
- Foreign keys must be enabled.
- The system must support automatic and manual backups.
- Backups must be integrity-checked.
- Notification failures must not prevent core work from being saved.

## Security

- Passwords must be hashed using a suitable password hashing function.
- User permissions must be enforced through application logic.
- Sensitive actions must be audit logged.
- Logs must not contain plaintext passwords.
- The application must avoid storing unnecessary sensitive data.
- Future API or cloud features must require a fresh security review.

## Maintainability

- Code must be modular.
- UI, controllers, business logic, database access, and infrastructure concerns must be separated.
- Naming must be clear and consistent.
- Documentation must be updated as the project evolves.
- Shared constants should be centralized.
- Complex workflows should have focused service tests.

## Usability

- The UI must be simple enough for non-technical office staff.
- Common workflows must require as few steps as practical.
- Screens must support search and filtering for real office data.
- Errors must be understandable and actionable.

## Performance

- Searchable database columns must be indexed where useful.
- Reports must avoid unnecessary full-table loading when possible.
- Long-running exports, backups, and notification sends should not freeze the UI.
- SQLite is expected to support the initial single-office deployment.

## Scalability

- Version 1.0 targets a single office.
- The architecture must keep future migration to PostgreSQL/MySQL possible.
- Business logic must not depend directly on SQLite-specific behavior.
- True multi-laptop concurrent usage should be treated as a later architecture milestone.

## Portability

- The application must run on Windows.
- The final release must be packaged as an executable.
- Runtime paths must be configurable and not hardcoded only to developer machines.

## Observability

- Application logs must capture startup, shutdown, errors, backups, reports, authentication events, and notification failures.
- Audit logs must capture business actions.
- Technical logs and audit logs must remain separate.

## Cost

- The project must use only free and open-source technologies unless a future feature is explicitly approved otherwise.

