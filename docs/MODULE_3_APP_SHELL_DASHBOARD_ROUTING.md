# Module 3: Application Shell and Dashboard Routing

## Current Step

Step 4: Testing and review.

## Purpose

Module 3 wires the foundation and authentication layers into a runnable desktop application flow.

The goal is not to build full dashboard metrics yet. The goal is to create the authenticated application shell and route users safely after login.

## Architecture Review

### Current Design

The project has:

- Core startup context.
- Database initialization.
- Authentication service.
- Login view.
- Reusable UI components.
- Window manager.
- Permission-aware navigation shell.

### Recommended Improvement

Add an application shell layer that coordinates:

- Startup database initialization.
- First-run admin flow.
- Login view.
- Authenticated navigation shell.
- Placeholder dashboard route.

### Advantages

- Gives the desktop app a real startup flow.
- Keeps routing separate from individual screens.
- Allows later dashboard/client/work modules to plug into navigation.
- Avoids hardcoding screen transitions inside the login view.

### Disadvantages

- Requires careful separation between app shell routing and business services.
- Placeholder dashboard must remain intentionally minimal to avoid starting the dashboard module early.

### Migration Required

No database migration is required.

## Module Scope

This module will create:

- Application shell controller or coordinator.
- Startup flow that initializes database before UI routing.
- Login route.
- Authenticated shell route.
- Placeholder dashboard content area.
- Navigation items filtered by permissions.
- Tests for route decisions where practical.

## Out of Scope

This module will not implement:

- Real dashboard metrics.
- Client management.
- Work allocation.
- Billing screens.
- Reports.
- WhatsApp automation.

## Routing Flow

```text
main.py
|
initialize_application()
|
initialize_database()
|
WindowManager
|
LoginView
|
AuthController
|
Authenticated App Shell
|
Placeholder Dashboard
```

## Navigation Strategy

Initial authenticated navigation should include only routes we can safely represent:

- Dashboard placeholder
- Settings placeholder if needed later

Future modules will add:

- Clients
- Work
- Staff
- Billing
- Collections
- Reports

Navigation visibility must use permission codes.

## Step Plan

### Step 1: Planning and Architecture Review

Create this document and confirm the shell approach.

### Step 2: UI Design

Define the shell layout using `Sidebar`, `TopBar`, and reusable content area.

### Step 3: Implementation

Wire `main.py` to initialize database and start the app shell.

### Step 4: Testing

Add tests for route selection and navigation item filtering where practical.

### Step 5: Improvements

Review startup errors, empty-state messaging, and user experience.

### Step 6: Git Commit

Commit the completed module.

## Acceptance Criteria

Module 3 is complete only when:

- App startup initializes core context and database.
- Login view can be shown by the window manager.
- Successful login routes to authenticated shell.
- Authenticated shell uses reusable navigation components.
- Placeholder dashboard is clearly marked as placeholder.
- No full dashboard metrics are implemented yet.
- Tests pass.
- Documentation is updated.
- Git commit is created.

## Implementation Notes

- `ApplicationShell` coordinates startup database initialization, login routing, and authenticated shell routing.
- `AppShell` provides the authenticated navigation shell.
- `DashboardPlaceholder` is intentionally minimal and does not implement real dashboard metrics.
- `main.py` now starts the GUI application shell after core startup.

## Risks and Controls

| Risk | Control |
| --- | --- |
| Dashboard scope creep | Keep dashboard as placeholder only |
| Tight coupling between login and shell | Route through coordinator/window manager |
| Permission drift | Use permission codes for navigation |
| Startup error confusion | Log technical details and show safe user messages |
