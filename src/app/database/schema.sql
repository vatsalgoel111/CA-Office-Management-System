PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_migrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    is_system_role INTEGER NOT NULL DEFAULT 1 CHECK (is_system_role IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS role_permissions (
    role_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    mobile TEXT,
    email TEXT,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles (id)
);

CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_name TEXT NOT NULL,
    business_name TEXT,
    mobile TEXT,
    email TEXT,
    pan TEXT,
    gstin TEXT,
    address TEXT,
    client_type TEXT,
    status TEXT NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'inactive')),
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS work_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    assigned_to_user_id INTEGER NOT NULL,
    assigned_by_user_id INTEGER NOT NULL,
    work_type TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT NOT NULL DEFAULT 'normal'
        CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (
            status IN (
                'pending',
                'in_progress',
                'waiting_for_client',
                'completed',
                'on_hold',
                'cancelled'
            )
        ),
    due_date TEXT,
    completed_at TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients (id),
    FOREIGN KEY (assigned_to_user_id) REFERENCES users (id),
    FOREIGN KEY (assigned_by_user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS remarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    work_item_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    remark_text TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (work_item_id) REFERENCES work_items (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS bills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    work_item_id INTEGER,
    bill_number TEXT NOT NULL UNIQUE,
    bill_date TEXT NOT NULL,
    amount_paise INTEGER NOT NULL CHECK (amount_paise >= 0),
    status TEXT NOT NULL DEFAULT 'unpaid'
        CHECK (status IN ('unpaid', 'partial', 'paid', 'cancelled')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients (id),
    FOREIGN KEY (work_item_id) REFERENCES work_items (id)
);

CREATE TABLE IF NOT EXISTS collections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_id INTEGER NOT NULL,
    received_amount_paise INTEGER NOT NULL CHECK (received_amount_paise > 0),
    received_date TEXT NOT NULL,
    payment_mode TEXT NOT NULL DEFAULT 'other'
        CHECK (payment_mode IN ('cash', 'bank', 'upi', 'cheque', 'other')),
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bill_id) REFERENCES bills (id)
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id INTEGER,
    old_values TEXT,
    new_values TEXT,
    description TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key TEXT NOT NULL UNIQUE,
    setting_value TEXT NOT NULL,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient_user_id INTEGER NOT NULL,
    related_work_item_id INTEGER,
    notification_type TEXT NOT NULL,
    provider TEXT NOT NULL DEFAULT 'manual',
    message TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'sent', 'failed', 'skipped')),
    failure_reason TEXT,
    retry_count INTEGER NOT NULL DEFAULT 0 CHECK (retry_count >= 0),
    sent_at TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recipient_user_id) REFERENCES users (id),
    FOREIGN KEY (related_work_item_id) REFERENCES work_items (id)
);

CREATE INDEX IF NOT EXISTS idx_users_role_id ON users (role_id);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users (is_active);

CREATE INDEX IF NOT EXISTS idx_clients_client_name ON clients (client_name);
CREATE INDEX IF NOT EXISTS idx_clients_business_name ON clients (business_name);
CREATE INDEX IF NOT EXISTS idx_clients_mobile ON clients (mobile);
CREATE INDEX IF NOT EXISTS idx_clients_pan ON clients (pan);
CREATE INDEX IF NOT EXISTS idx_clients_gstin ON clients (gstin);
CREATE INDEX IF NOT EXISTS idx_clients_status ON clients (status);

CREATE INDEX IF NOT EXISTS idx_work_items_client_id ON work_items (client_id);
CREATE INDEX IF NOT EXISTS idx_work_items_assigned_to ON work_items (assigned_to_user_id);
CREATE INDEX IF NOT EXISTS idx_work_items_assigned_by ON work_items (assigned_by_user_id);
CREATE INDEX IF NOT EXISTS idx_work_items_status ON work_items (status);
CREATE INDEX IF NOT EXISTS idx_work_items_due_date ON work_items (due_date);
CREATE INDEX IF NOT EXISTS idx_work_items_assignee_status
    ON work_items (assigned_to_user_id, status);
CREATE INDEX IF NOT EXISTS idx_work_items_status_due_date
    ON work_items (status, due_date);

CREATE INDEX IF NOT EXISTS idx_remarks_work_item_id ON remarks (work_item_id);
CREATE INDEX IF NOT EXISTS idx_remarks_user_id ON remarks (user_id);

CREATE INDEX IF NOT EXISTS idx_bills_client_id ON bills (client_id);
CREATE INDEX IF NOT EXISTS idx_bills_work_item_id ON bills (work_item_id);
CREATE INDEX IF NOT EXISTS idx_bills_bill_date ON bills (bill_date);
CREATE INDEX IF NOT EXISTS idx_bills_status ON bills (status);

CREATE INDEX IF NOT EXISTS idx_collections_bill_id ON collections (bill_id);
CREATE INDEX IF NOT EXISTS idx_collections_received_date ON collections (received_date);
CREATE INDEX IF NOT EXISTS idx_collections_payment_mode ON collections (payment_mode);

CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs (user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs (action);
CREATE INDEX IF NOT EXISTS idx_audit_logs_entity ON audit_logs (entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs (created_at);

CREATE INDEX IF NOT EXISTS idx_notifications_recipient
    ON notifications (recipient_user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_work_item
    ON notifications (related_work_item_id);
CREATE INDEX IF NOT EXISTS idx_notifications_status ON notifications (status);
CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications (created_at);

INSERT OR IGNORE INTO schema_migrations (version, name)
VALUES ('0001', 'initial_schema');

