# Database Design

SQLite will be the permanent database for Version 1.0.

## Design Principles

- Use normalized tables for core business data.
- Use foreign keys for relationships.
- Use timestamps for important records.
- Use soft deactivation where business history must be preserved.
- Use audit logs for sensitive actions.
- Use indexes for frequent search and report filters.
- Keep database access isolated so future PostgreSQL or MySQL migration remains practical.

## Normalization Review

The current design is normalized enough for Version 1.0:

- Users, clients, work items, remarks, bills, collections, audit logs, settings, and notifications are separate tables.
- Repeating work remarks are not stored inside `work_items`; they are stored in `remarks`.
- Collections are not stored as columns on bills; they are separate payment records.
- Notifications are stored separately from business records.

Future improvement candidates:

- Move `work_type`, `client_type`, `priority`, and `status` into lookup tables if the office needs configurable values.
- Add a `schema_migrations` table before the first production release.

## Migration Readiness

To keep future PostgreSQL/MySQL migration possible:

- Services must not use SQLite-specific SQL.
- Repositories must keep SQL isolated.
- Avoid SQLite-only features unless wrapped behind repository or database adapter methods.
- Use ISO date strings in Version 1.0, but keep date handling centralized.
- Avoid storing business-critical values in loosely formatted text when structured columns are better.

## Tables

### roles

Stores role definitions.

| Column | Type | Notes |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | Unique role ID |
| name | TEXT | Unique role name |
| description | TEXT | Optional |
| is_system_role | INTEGER | 1 for built-in roles |
| created_at | TEXT | ISO timestamp |
| updated_at | TEXT | ISO timestamp |

Initial roles:

- Administrator
- Manager
- Staff
- Accountant
- Read Only

Version 1.0 may expose only Administrator and Staff in the UI, but the database supports future roles from the beginning.

### permissions

Stores permission definitions.

| Column | Type | Notes |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | Unique permission ID |
| code | TEXT | Unique permission code |
| description | TEXT | Optional |
| created_at | TEXT | ISO timestamp |

### role_permissions

Maps roles to permissions.

| Column | Type | Notes |
| --- | --- | --- |
| role_id | INTEGER | References roles.id |
| permission_id | INTEGER | References permissions.id |
| created_at | TEXT | ISO timestamp |

The composite primary key should be `role_id, permission_id`.

### users

Stores login users and staff profile data.

| Column | Type | Notes |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | Unique user ID |
| full_name | TEXT | Required |
| username | TEXT | Unique, required |
| password_hash | TEXT | Required |
| role_id | INTEGER | References roles.id |
| mobile | TEXT | Optional |
| email | TEXT | Optional |
| is_active | INTEGER | 1 active, 0 inactive |
| created_at | TEXT | ISO timestamp |
| updated_at | TEXT | ISO timestamp |

Indexes:

- Unique index on `username`.
- Index on `role_id`.
- Index on `is_active`.

### clients

Stores client master data.

| Column | Type | Notes |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | Unique client ID |
| client_name | TEXT | Required |
| business_name | TEXT | Optional |
| mobile | TEXT | Optional |
| email | TEXT | Optional |
| pan | TEXT | Optional |
| gstin | TEXT | Optional |
| address | TEXT | Optional |
| client_type | TEXT | Individual, firm, company, etc. |
| status | TEXT | active or inactive |
| notes | TEXT | Optional |
| created_at | TEXT | ISO timestamp |
| updated_at | TEXT | ISO timestamp |

Indexes:

- Index on `client_name`.
- Index on `business_name`.
- Index on `mobile`.
- Index on `pan`.
- Index on `gstin`.
- Index on `status`.

### work_items

Stores assigned office work.

| Column | Type | Notes |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | Unique work item ID |
| client_id | INTEGER | References clients.id |
| assigned_to_user_id | INTEGER | References users.id |
| assigned_by_user_id | INTEGER | References users.id |
| work_type | TEXT | GST, ITR, audit, etc. |
| title | TEXT | Required |
| description | TEXT | Optional |
| priority | TEXT | low, normal, high, urgent |
| status | TEXT | pending, in_progress, waiting_for_client, completed, on_hold, cancelled |
| due_date | TEXT | ISO date |
| completed_at | TEXT | Nullable |
| created_at | TEXT | ISO timestamp |
| updated_at | TEXT | ISO timestamp |

Indexes:

- Index on `client_id`.
- Index on `assigned_to_user_id`.
- Index on `assigned_by_user_id`.
- Index on `status`.
- Index on `due_date`.
- Composite index on `assigned_to_user_id, status`.
- Composite index on `status, due_date`.

### remarks

Stores task comments and progress notes.

| Column | Type | Notes |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | Unique remark ID |
| work_item_id | INTEGER | References work_items.id |
| user_id | INTEGER | References users.id |
| remark_text | TEXT | Required |
| created_at | TEXT | ISO timestamp |

Indexes:

- Index on `work_item_id`.
- Index on `user_id`.

### bills

Stores billing records.

| Column | Type | Notes |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | Unique bill ID |
| client_id | INTEGER | References clients.id |
| work_item_id | INTEGER | Nullable reference to work_items.id |
| bill_number | TEXT | Unique |
| bill_date | TEXT | ISO date |
| amount_paise | INTEGER | Required, stores amount in paise |
| status | TEXT | unpaid, partial, paid, cancelled |
| created_at | TEXT | ISO timestamp |
| updated_at | TEXT | ISO timestamp |

Indexes:

- Unique index on `bill_number`.
- Index on `client_id`.
- Index on `work_item_id`.
- Index on `bill_date`.
- Index on `status`.

Money note: amounts are stored as integer paise instead of floating-point values. This avoids rounding errors in billing and collection calculations.

### collections

Stores payment collection records.

| Column | Type | Notes |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | Unique collection ID |
| bill_id | INTEGER | References bills.id |
| received_amount_paise | INTEGER | Required, stores amount in paise |
| received_date | TEXT | ISO date |
| payment_mode | TEXT | cash, bank, upi, cheque, other |
| notes | TEXT | Optional |
| created_at | TEXT | ISO timestamp |

Indexes:

- Index on `bill_id`.
- Index on `received_date`.
- Index on `payment_mode`.

### audit_logs

Stores important system activity.

| Column | Type | Notes |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | Unique log ID |
| user_id | INTEGER | Nullable reference to users.id |
| action | TEXT | Required |
| entity_type | TEXT | Example: client, work_item, bill |
| entity_id | INTEGER | Nullable |
| old_values | TEXT | JSON text, nullable |
| new_values | TEXT | JSON text, nullable |
| description | TEXT | Human-readable activity |
| created_at | TEXT | ISO timestamp |

Indexes:

- Index on `user_id`.
- Index on `action`.
- Index on `entity_type, entity_id`.
- Index on `created_at`.

Audit note: audit logs are append-only. The application must not expose normal delete/edit flows for audit entries.

### settings

Stores configurable system settings.

| Column | Type | Notes |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | Unique setting ID |
| setting_key | TEXT | Unique |
| setting_value | TEXT | Required |
| updated_at | TEXT | ISO timestamp |

Indexes:

- Unique index on `setting_key`.

### notifications

Stores notification history.

| Column | Type | Notes |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | Unique notification ID |
| recipient_user_id | INTEGER | References users.id |
| related_work_item_id | INTEGER | Nullable reference to work_items.id |
| notification_type | TEXT | whatsapp, reminder, summary |
| provider | TEXT | whatsapp_web, manual, future_api |
| message | TEXT | Required |
| status | TEXT | pending, sent, failed, skipped |
| failure_reason | TEXT | Nullable |
| retry_count | INTEGER | Defaults to 0 |
| sent_at | TEXT | Nullable |
| created_at | TEXT | ISO timestamp |

Indexes:

- Index on `recipient_user_id`.
- Index on `related_work_item_id`.
- Index on `status`.
- Index on `created_at`.

### schema_migrations

Tracks database schema versions.

| Column | Type | Notes |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | Unique migration row |
| version | TEXT | Unique migration version |
| name | TEXT | Migration name |
| applied_at | TEXT | ISO timestamp |

## Backup and Recovery Data Rules

- Backups must copy the database only after writes are complete.
- Backups must include a timestamp.
- Recovery must be tested by opening the copied database and running integrity checks.
- Backup metadata should be logged.
