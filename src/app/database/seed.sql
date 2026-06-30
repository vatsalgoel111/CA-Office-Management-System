PRAGMA foreign_keys = ON;

INSERT OR IGNORE INTO roles (code, name, description, is_system_role)
VALUES
    ('administrator', 'Administrator', 'Full system access.', 1),
    ('manager', 'Manager', 'Supervises work and staff with limited settings access.', 1),
    ('staff', 'Staff', 'Can view and update assigned work.', 1),
    ('accountant', 'Accountant', 'Can manage billing and collections.', 1),
    ('read_only', 'Read Only', 'Can view records without modifying data.', 1);

INSERT OR IGNORE INTO permissions (code, description)
VALUES
    ('users.manage', 'Manage users and staff accounts.'),
    ('clients.view', 'View client records.'),
    ('clients.create', 'Create client records.'),
    ('clients.update', 'Update client records.'),
    ('clients.deactivate', 'Deactivate client records.'),
    ('work.view_all', 'View all work items.'),
    ('work.view_assigned', 'View assigned work items.'),
    ('work.assign', 'Assign work to staff.'),
    ('work.update_status', 'Update work status.'),
    ('billing.manage', 'Manage bills.'),
    ('collections.manage', 'Manage collections.'),
    ('reports.view', 'View reports.'),
    ('settings.manage', 'Manage application settings.'),
    ('audit.view', 'View audit logs.'),
    ('backup.create', 'Create backups.');

INSERT OR IGNORE INTO role_permissions (role_id, permission_id)
SELECT roles.id, permissions.id
FROM roles
CROSS JOIN permissions
WHERE roles.code = 'administrator';

INSERT OR IGNORE INTO role_permissions (role_id, permission_id)
SELECT roles.id, permissions.id
FROM roles
JOIN permissions ON permissions.code IN (
    'clients.view',
    'clients.create',
    'clients.update',
    'work.view_all',
    'work.assign',
    'work.update_status',
    'reports.view'
)
WHERE roles.code = 'manager';

INSERT OR IGNORE INTO role_permissions (role_id, permission_id)
SELECT roles.id, permissions.id
FROM roles
JOIN permissions ON permissions.code IN (
    'clients.view',
    'work.view_assigned',
    'work.update_status'
)
WHERE roles.code = 'staff';

INSERT OR IGNORE INTO role_permissions (role_id, permission_id)
SELECT roles.id, permissions.id
FROM roles
JOIN permissions ON permissions.code IN (
    'clients.view',
    'billing.manage',
    'collections.manage',
    'reports.view'
)
WHERE roles.code = 'accountant';

INSERT OR IGNORE INTO role_permissions (role_id, permission_id)
SELECT roles.id, permissions.id
FROM roles
JOIN permissions ON permissions.code IN (
    'clients.view',
    'work.view_all',
    'reports.view'
)
WHERE roles.code = 'read_only';

INSERT OR IGNORE INTO settings (setting_key, setting_value)
VALUES
    ('app.theme', 'dark'),
    ('backup.auto_enabled', 'true'),
    ('backup.frequency', 'daily'),
    ('notifications.whatsapp_enabled', 'false');

