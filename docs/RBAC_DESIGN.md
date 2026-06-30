# Role-Based Access Control Design

## Purpose

The system must support simple roles in Version 1.0 while allowing future expansion without redesign.

Version 1.0 may expose only Administrator and Staff in the UI, but the internal design should support more roles and permissions.

## Planned Roles

### Administrator

Full system access.

### Manager

Future role for supervising work and staff without full system configuration access.

### Staff

Can view and update assigned work.

### Accountant

Future role for billing, collections, and financial reports.

### Read Only

Future role for users who can view records but cannot modify data.

## Design Approach

Use role-based access first, with permission-ready architecture.

Version 1.0 database should support:

- `roles`
- `permissions`
- `role_permissions`
- `users.role_id`

This is slightly more work than storing only `administrator` or `staff` text on the user record, but it avoids redesign later.

## Why Not Hardcode Only Admin and Staff

Hardcoding two roles is fast, but it creates technical debt. CA offices often grow into more nuanced access needs:

- A manager may assign work but not change settings.
- An accountant may manage collections but not staff.
- A read-only user may need report access only.

## Service Layer Rule

Permissions must be checked in services, not only in the UI.

Reason: hiding a button is not security. Business operations must reject unauthorized actions even if called directly from a controller or future API.

## Version 1.0 Permission Examples

Initial permissions may include:

- `users.manage`
- `clients.view`
- `clients.create`
- `clients.update`
- `clients.deactivate`
- `work.view_all`
- `work.view_assigned`
- `work.assign`
- `work.update_status`
- `billing.manage`
- `collections.manage`
- `reports.view`
- `settings.manage`
- `audit.view`
- `backup.create`

