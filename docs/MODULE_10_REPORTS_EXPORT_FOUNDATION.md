# Module 10: Reports and Export Foundation

## Current Step

Completed.

## Purpose

Module 10 adds read-only operational reports and dependency-free CSV export.

## Architecture Review

### Current Design

The application already has normalized data for clients, work, bills, and collections. The Reports navigation item existed but showed a placeholder.

### Decision

Build report queries through a repository, protect them through a service, and export CSV files into configured runtime export paths.

## Why

- Reports should be read-only and isolated from transactional workflows.
- CSV export gives immediate practical value without adding dependencies.
- Centralized paths keep development, testing, and production exports separate.

## Module Scope

- Report table and export result models.
- Report repository with client, work, outstanding bill, and collection summaries.
- Report service with `reports.view` permission checks and CSV export.
- Report controller.
- Report preview/export UI.
- Reports route in the authenticated shell.
- Integration tests for report rows, CSV export, permissions, and validation.

## Out of Scope

- Styled Excel workbooks.
- PDF reports.
- Charts.
- Date range filters.
- Scheduled report generation.

## Acceptance Criteria

- Reports follow model/repository/service/controller/view layers. Completed.
- Report access requires `reports.view`. Completed.
- CSV exports use configured runtime export paths. Completed.
- Report queries are read-only. Completed.
- Tests pass. Completed.
- Module review is documented. Completed.
- Git commit is created. Pending until final verification.
