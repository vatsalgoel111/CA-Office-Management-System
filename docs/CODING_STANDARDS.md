# Coding Standards

## Python

- Follow PEP 8.
- Use meaningful names.
- Prefer small functions with one clear responsibility.
- Use type hints where useful.
- Use docstrings for public services and complex functions.
- Avoid duplicate logic.
- Avoid global mutable state.
- Use logging instead of print statements.

## Python File Header

Every new Python file should include a concise professional header when it adds meaningful project code.

Template:

```python
"""
File Purpose: Short explanation of what this file provides.
Module: app.<module_name>
Author: CA Office CMS Development Team
Created Date: YYYY-MM-DD
Last Modified: YYYY-MM-DD
Dependencies: Standard library and project dependencies used by this file.
"""
```

Rules:

- Keep the header short and useful.
- Do not add noisy comments throughout the file.
- Empty `__init__.py` files may use a one-line docstring instead of the full header.
- Update `Last Modified` when making meaningful changes to the file.

## Database

- Use parameterized SQL.
- Use transactions for important writes.
- Keep schema changes intentional and documented.
- Preserve business history where needed.
- Avoid hard deletes for records that affect auditability.

## UI

- Keep screens simple and staff-friendly.
- Avoid clutter.
- Validate input before saving.
- Show clear error messages.
- Use consistent spacing, colors, and typography.
- Support dark mode.

## Errors and Logging

- Catch exceptions at appropriate boundaries.
- Log technical details.
- Show user-friendly messages in the UI.
- Do not expose stack traces to normal users.

## Testing

- Write focused tests for services and repositories.
- Prefer testing business logic outside the UI first.
- Add regression tests when fixing bugs.

## Module Review Standard

At the end of every completed module, provide:

- What was completed
- Files created
- Files modified
- Architecture decisions
- Why those decisions were made
- Risks
- Suggested improvements
- Testing performed
- Git commit message
- Next module
