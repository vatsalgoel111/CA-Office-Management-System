# Deployment Plan

## Development Mode

During development, the app will run from source code.

## Production Mode

Version 1.0 will be packaged as a Windows executable using PyInstaller.

## Production Directory Strategy

The application should store runtime data outside the source code folder.

Recommended production layout:

```text
C:\CAOfficeCMS\
|-- CAOfficeCMS.exe
|-- data\
|   `-- database.sqlite3
|-- backups\
|-- exports\
`-- logs\
```

## SQLite Deployment Warning

SQLite is reliable for a local desktop application. It is not ideal for multiple staff laptops writing to the same database file over a network share.

Version 1.0 should use one of these safe deployment models:

- Single-machine office deployment.
- Main/server laptop with controlled access.
- Remote desktop access to the main machine.

Before true concurrent staff-laptop usage, we should add a small server API or migrate to PostgreSQL/MySQL.

## Backup Strategy

Backups should be timestamped:

```text
backup_YYYY_MM_DD_HHMMSS.sqlite3
```

Minimum backup behavior:

- Automatic daily backup.
- Manual backup button.
- Configurable backup folder.
- Integrity check after backup.
- Clear success or failure logging.
- Recovery instructions in the user manual before production release.

## Recovery Strategy

Recovery should follow a controlled process:

1. Close the application.
2. Copy the current database to a temporary safety folder.
3. Replace the active database with a selected backup.
4. Run an integrity check.
5. Start the application and verify login and dashboard counts.

## Logging in Production

Production logs should rotate to prevent unlimited growth.

Recommended:

- Keep application logs in `C:\CAOfficeCMS\logs\`.
- Use date or size-based rotation.
- Do not log plaintext passwords.
- Do not log confidential client documents.

## Deployment Checklist

- Build executable.
- Verify database path.
- Verify backup path.
- Verify log path.
- Verify app starts on target machine.
- Verify login.
- Verify database integrity check.
- Verify backup creation.
- Verify restore process using test data.
- Verify sample Excel export.
- Verify sample PDF export.
- Verify notification failure does not crash the app.

