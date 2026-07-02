# Module 8: Billing Management Foundation

## Current Step

Completed.

## Purpose

Module 8 adds bill creation, listing, and bill status tracking.

## Architecture Review

### Current Design

The database already includes normalized `bills` and `collections` tables. Dashboard outstanding amounts are calculated from bills minus collections.

### Decision

Billing is implemented as a separate module from collections.

## Why

- A bill is an amount raised to a client.
- A collection is money received against a bill.
- Separating them keeps accounting history accurate and supports partial payments.
- Future invoice PDF generation can build on bills without depending on collection workflow.

## Module Scope

- Billing models.
- Billing repository.
- Billing service with `billing.manage` permission checks.
- Billing controller.
- Billing view and route.
- Bill creation, listing, search, and status update.
- Integration tests for billing workflow and validation.

## Out of Scope

- Collection/payment entry.
- Invoice PDF generation.
- GST/tax computation.
- Bill edit/delete workflow.

## Acceptance Criteria

- Billing follows model/repository/service/controller/view layers. Completed.
- Only users with `billing.manage` can access billing workflows. Completed.
- Bill amount and date are validated before persistence. Completed.
- Duplicate bill numbers are rejected before database insertion. Completed.
- Bill status update is validated. Completed.
- Tests pass. Completed.
- Module review is documented. Completed.
- Git commit is created. Pending until final verification.
