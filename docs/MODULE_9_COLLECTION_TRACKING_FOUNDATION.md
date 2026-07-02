# Module 9: Collection Tracking Foundation

## Current Step

Completed.

## Purpose

Module 9 records client payments against bills and updates bill status automatically.

## Architecture Review

### Current Design

Billing stores raised amounts in `bills`. Payments are stored separately in `collections`.

### Decision

Collections are implemented as a separate clean architecture module.

## Why

- Partial payments are common in CA offices.
- Outstanding balance should be calculated from bills minus collections.
- Keeping collections separate preserves accounting history.

## Module Scope

- Collection domain models.
- Collection repository.
- Collection service with `collections.manage` permission checks.
- Collection controller.
- Collection view and route.
- Payment entry, listing, search, and bill status recalculation.
- Integration tests for partial payment, full payment, validation, and permissions.

## Out of Scope

- Receipt PDF generation.
- Payment reversal/correction workflow.
- Advanced ageing reports.
- Bank reconciliation.

## Acceptance Criteria

- Collections follow model/repository/service/controller/view layers. Completed.
- Only users with `collections.manage` can record collections. Completed.
- Over-collection is prevented. Completed.
- Cancelled bills cannot receive collections. Completed.
- Bill status changes to `partial` or `paid` after collection entry. Completed.
- Tests pass. Completed.
- Module review is documented. Completed.
- Git commit is created. Pending until final verification.
