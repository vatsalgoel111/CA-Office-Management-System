# Functional Requirements

## Login

- Users must log in with username and password.
- Passwords must be stored as secure hashes.
- Inactive users must not be allowed to log in.
- Failed login attempts must be logged.

## Role-Based Access

Version 1.0 will expose Administrator and Staff as the primary roles, but the permission system must support future roles without redesign.

### Administrator

The administrator can:

- Manage clients
- Manage staff
- Assign work
- View all work
- Update work
- View reports
- Manage bills and collections
- View audit logs
- Configure settings
- Create backups

### Staff

Staff can:

- View assigned work
- Update assigned work status
- Add remarks to assigned work
- View limited client information needed for work
- View own work history

Staff cannot:

- Delete clients
- Manage users
- View all financial reports unless permission is added later
- Change system settings

Future supported roles:

- Manager
- Accountant
- Read Only

Permission checks must be enforced in the service layer, not only by hiding UI controls.

## Client Management

The system must allow authorized users to:

- Add clients
- Edit clients
- Search clients
- Deactivate clients
- Import clients from Excel

## Work Allocation

The system must allow administrators to:

- Assign work to staff
- Set due date
- Set priority
- Track status
- View work history

## Billing and Collections

The system must allow authorized users to:

- Create bills
- Link bills to clients and work items
- Record payments
- Track outstanding balances

## Reports

The system must generate:

- Pending work report
- Completed work report
- Overdue work report
- Staff-wise work report
- Client-wise work report
- Billing report
- Collection report
- Outstanding amount report

Reports must support Excel and PDF export where appropriate.

## Automation

The system must support:

- Audit logging
- Automatic database backup
- Daily pending work summary
- Overdue work reminders
- WhatsApp notifications for work assignment and status updates
