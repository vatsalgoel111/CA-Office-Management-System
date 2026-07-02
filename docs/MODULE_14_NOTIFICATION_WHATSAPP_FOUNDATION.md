# Module 14: Notification and WhatsApp Foundation

## Current Step

Completed.

## Purpose

Module 14 adds a provider-neutral notification queue and WhatsApp-ready message records.

## Architecture Review

### Current Design

The initial schema already includes `notifications` and notification settings.

### Decision

Queue notification records now and defer real WhatsApp delivery until a provider is configured.

## Why

- WhatsApp delivery must be implemented through a compliant provider or explicit manual workflow.
- Business modules can queue intent without depending on a provider SDK.
- Failed/sent/retry tracking belongs in the database.

## Module Scope

- Notification models.
- Notification repository.
- Notification service.
- Notification controller.
- Notification queue view and route.
- Tests for queueing, WhatsApp provider tagging, validation, and permissions.

## Out of Scope

- Real WhatsApp API sending.
- WhatsApp Web/browser automation.
- Retry worker.
- Notification templates.

## Acceptance Criteria

- Notifications follow model/repository/service/controller/view layers. Completed.
- WhatsApp messages are queued, not sent directly. Completed.
- Notification management requires `settings.manage`. Completed.
- Tests pass. Completed.
- Module review is documented. Completed.
- Git commit is created. Pending until final verification.
