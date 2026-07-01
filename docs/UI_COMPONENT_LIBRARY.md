# UI Component Library

The reusable UI component library lives under `src/app/ui/`.

All future screens must reuse these components instead of creating ad hoc CustomTkinter widgets repeatedly.

## Implementation Order

1. Theme Manager
2. Reusable UI Component Library
3. Window Manager
4. Navigation Framework
5. Login Screen
6. Dashboard

Only items 1 to 4 are part of the current UI foundation step. Login and dashboard screens are not implemented yet.

## Files

| File | Purpose |
| --- | --- |
| `theme.py` | Semantic design tokens and CustomTkinter theme application |
| `components.py` | Shared widgets such as buttons, cards, forms, tables, badges, dialogs, and notifications |
| `window_manager.py` | Root window configuration and view registration |
| `navigation.py` | Permission-aware navigation item model and navigation shell primitives |

## Component Rules

- Future screens must use shared components where possible.
- Components must consume semantic design tokens instead of hardcoded colors.
- UI files must not contain SQL queries.
- Navigation must remain permission-aware.
- Screen modules should focus on layout and workflow, not widget styling.

## Initial Components

- `PrimaryButton`
- `SecondaryButton`
- `IconButton`
- `SearchBox`
- `DataTable`
- `Sidebar`
- `TopBar`
- `StatusBadge`
- `InfoCard`
- `ConfirmationDialog`
- `LoadingOverlay`
- `NotificationToast`
- `FormField`

