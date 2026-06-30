# Software Requirement Specification

## 1. Introduction

The CA Office Management System is a Windows desktop application for Chartered Accountant offices. It will replace shared Excel-based tracking with a structured SQLite-backed application while keeping the workflow simple for office staff.

Excel will remain part of the workflow only for importing existing data and exporting reports.

## 2. Product Scope

The software will manage clients, staff, work allocation, task progress, remarks, bills, collections, reminders, reports, audit logs, backups, and WhatsApp notifications.

## 3. Target Users

- Chartered Accountant or office administrator
- Office staff

## 4. Goals

- Reduce dependency on shared Excel files.
- Improve work visibility and accountability.
- Track pending, overdue, and completed work.
- Track billing and collections.
- Preserve activity history through audit logs.
- Provide reliable backups.
- Support practical office automation.

## 5. Constraints

- Must run on Windows.
- Must use free and open-source technologies.
- Must use SQLite as the permanent database.
- Must not depend on Excel as the primary data store.
- Must be maintainable for long-term commercial use.

## 6. In Scope for Version 1.0

- Login system
- Role-based access
- Dashboard
- Client management
- Staff management
- Work allocation
- Task status updates
- Remarks
- Bill tracking
- Collection tracking
- Search and filters
- Reports
- Audit log
- Automatic backup
- Reminder system
- WhatsApp notifications
- Settings
- Dark mode
- Excel import/export
- PDF report generation
- Windows executable packaging

## 7. Out of Scope for Version 1.0

- Mobile app
- Cloud sync
- Client portal
- Document management
- Attendance
- Leave management
- AI assistant
- Email notifications

These are future expansion areas and should not complicate Version 1.0.

