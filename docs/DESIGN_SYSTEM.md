# Design System

This document is the single source of truth for future CA Office CMS user interface work.

No UI screens are implemented here. This file defines standards only.

## Design Principles

- Professional, calm, and trustworthy.
- Built for repeated office use, not marketing.
- Dense enough for real CA office work without becoming cluttered.
- Clear hierarchy for pending, overdue, completed, and financial information.
- Accessible contrast and readable text in both light and dark themes.

## Color Palette

### Brand Colors

| Token | Light | Dark | Usage |
| --- | --- | --- | --- |
| `color.primary` | `#1F6F78` | `#3AA6B2` | Primary actions, active navigation |
| `color.primary_hover` | `#185D65` | `#2E8E99` | Primary hover states |
| `color.secondary` | `#334155` | `#CBD5E1` | Secondary text and controls |
| `color.accent` | `#B7791F` | `#F6AD55` | Financial highlights |

### Neutral Colors

| Token | Light | Dark | Usage |
| --- | --- | --- | --- |
| `color.bg` | `#F8FAFC` | `#101418` | Main window background |
| `color.surface` | `#FFFFFF` | `#171C22` | Panels, cards, tables |
| `color.surface_alt` | `#EEF2F7` | `#202833` | Sidebar, table headers |
| `color.border` | `#D7DEE8` | `#344050` | Dividers and input borders |
| `color.text` | `#172033` | `#E5E7EB` | Primary text |
| `color.text_muted` | `#64748B` | `#9CA3AF` | Secondary text |

### Status Colors

| Status | Light | Dark | Usage |
| --- | --- | --- | --- |
| Success | `#15803D` | `#4ADE80` | Completed, paid, backup success |
| Warning | `#B45309` | `#FBBF24` | Due soon, partial payment |
| Error | `#B91C1C` | `#F87171` | Overdue, failed, unpaid critical |
| Info | `#0369A1` | `#38BDF8` | General notifications |
| Neutral | `#64748B` | `#94A3B8` | On hold, inactive |

## Typography

- Primary font: Windows system UI.
- Fallbacks: `Segoe UI`, `Arial`, `sans-serif`.
- Base text: `14px`.
- Small text: `12px`.
- Section heading: `18px`.
- Page heading: `22px`.
- Dashboard metric: `24px`.
- Use regular and semibold weights.
- Avoid decorative fonts.

## Spacing System

Use an 8px spacing rhythm.

| Token | Value | Usage |
| --- | --- | --- |
| `space.1` | `4px` | Tight icon/text spacing |
| `space.2` | `8px` | Standard inner spacing |
| `space.3` | `12px` | Form field gaps |
| `space.4` | `16px` | Panel padding |
| `space.5` | `24px` | Section spacing |
| `space.6` | `32px` | Major layout spacing |

## Buttons

### Primary Button

- Use for save, assign, create, and export actions.
- Filled with `color.primary`.
- Text must be short and action-oriented.
- Disabled state must be visually clear.

### Secondary Button

- Use for cancel, reset, filter, and less frequent actions.
- Neutral surface with visible border.

### Danger Button

- Use only for destructive or deactivation actions.
- Confirm destructive actions in a dialog.

### Icon Buttons

- Use for compact table actions.
- Add tooltip text when tooltips are implemented.
- Keep icon style consistent.

## Input Fields

- Labels above fields.
- Required fields marked consistently.
- Validation shown near the field.
- Avoid placeholder-only labels.
- Use consistent height across text inputs, dropdowns, and date fields.
- Read-only fields must look different from editable fields.

## Tables and Grids

Tables are primary work surfaces.

Standards:

- Clear headers.
- Subtle alternating row backgrounds may be used.
- Status columns use colored text labels.
- Numeric columns align right.
- Date columns use one consistent format.
- Row actions stay at the far right.
- Search and filters sit above the table.
- Empty states should explain what is missing.

## Cards

Cards are used for dashboard metrics and compact summaries.

Rules:

- Border radius: maximum `8px`.
- Avoid nesting cards inside cards.
- Use cards for grouped content, not full page sections.
- Keep metric cards compact and scannable.

## Sidebar

The sidebar is the main navigation pattern.

Standards:

- Width: approximately `220px` on desktop.
- Active item uses primary color or clear active background.
- Navigation labels must be stable and business-friendly.
- Admin-only items should be permission-aware.
- Sidebar collapse is optional and should be added only if useful.

## Navigation

Primary navigation:

- Dashboard
- Clients
- Work
- Staff
- Billing
- Collections
- Reports
- Settings

Future navigation must be permission-aware.

## Dialogs

Use dialogs for:

- Confirming destructive actions.
- Short create/edit workflows when a full page is unnecessary.
- Error details when a simple message is not enough.

Rules:

- Clear title.
- One primary action.
- One cancel or close action.
- Avoid long complex forms inside small dialogs.

## Notifications

Use non-blocking notifications for:

- Save success.
- Export complete.
- Backup complete.
- Notification queued.

Use blocking dialogs for:

- Destructive confirmations.
- Critical startup errors.
- Database or backup failures needing user attention.

## Status Labels

Use consistent labels:

- Pending
- In Progress
- Waiting for Client
- Completed
- On Hold
- Cancelled
- Overdue
- Paid
- Partial
- Unpaid

Status labels must use text and color. Never rely on color alone.

## Icons

- Use simple line icons where available.
- Icons must support business clarity, not decoration.
- Avoid mixing icon styles.

Common icon concepts:

- Dashboard
- Clients
- Work
- Staff
- Billing
- Reports
- Settings
- Search
- Export
- Backup
- Edit
- Deactivate

## Light and Dark Theme Strategy

Dark mode is required, but light mode should remain available.

Rules:

- Define colors as semantic tokens.
- UI components should consume tokens.
- Avoid hardcoded colors in feature code.
- Test contrast in both themes.
- Maintain neutral, primary, accent, and status colors.

## Responsive Behavior

The app targets Windows desktop first.

Expected sizes:

- Minimum practical width: `1024px`.
- Preferred width: `1280px` and above.
- Important tables should resize horizontally.
- Forms may use one column at narrow widths and two columns at wider widths.
- Text must not overlap or hide critical business data.

## Accessibility

- Maintain readable contrast.
- Do not rely on color alone for status.
- Use clear labels for inputs.
- Support keyboard navigation where practical.
- Keep focus states visible.
- Avoid tiny click targets.
- Error messages should be specific and actionable.

## UI Component Naming

Use names that match the business domain.

View examples:

- `DashboardView`
- `ClientListView`
- `ClientFormDialog`
- `WorkAllocationView`
- `WorkStatusBadge`
- `BillingSummaryCard`
- `ReportFilterPanel`
- `SidebarNavigation`
- `AppNotification`

Controller examples:

- `DashboardController`
- `ClientController`
- `WorkController`
- `BillingController`
- `ReportController`

## Implementation Rule

Future UI code must follow this document unless a change is intentionally proposed, explained, and approved.

