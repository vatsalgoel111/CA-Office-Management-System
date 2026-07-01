# Module 4: Dashboard Foundation

## Current Step

Step 1 through Step 5: implementation in progress.

## Purpose

Module 4 replaces the placeholder dashboard with real dashboard summary data while preserving clean architecture boundaries.

The dashboard must stay information-dense and office-friendly, but it must not become a place where business logic is calculated in the UI.

## Architecture Review

### Current Design

The application shell routes authenticated users to a placeholder dashboard. The database already contains clients, work items, bills, collections, users, and permissions.

### Recommended Improvement

Add dashboard-specific model, repository, service, controller, and view.

```text
DashboardView
|
DashboardController
|
DashboardService
|
DashboardRepository
|
Database Adapter
```

### Advantages

- Dashboard UI remains simple.
- Metrics are testable without launching the GUI.
- Future dashboard widgets can be added incrementally.
- Repository SQL remains isolated.

### Disadvantages

- More files than calculating counts directly in the view.
- Requires service tests to keep behavior clear.

### Migration Required

No database migration is required.

## Module Scope

This module creates:

- Dashboard summary model.
- Dashboard repository.
- Dashboard service.
- Dashboard controller.
- Dashboard view using reusable UI components.
- Tests for dashboard summary behavior.

## Out of Scope

This module does not implement:

- Charts.
- Report exports.
- Detailed drill-down screens.
- Client management.
- Work allocation.
- Billing workflows.

## Metrics

Initial metrics:

- Active clients.
- Pending work.
- Overdue work.
- Completed work.
- Unpaid bills.
- Outstanding amount.

For staff users, work metrics are limited to assigned work unless they have `work.view_all`.

## Acceptance Criteria

- Dashboard uses service/controller/repository layers.
- Dashboard view uses reusable `InfoCard` components.
- No SQL appears in dashboard UI.
- Staff work counts respect permissions.
- Tests pass.
- Module review is documented.
- Git commit is created.

