"""
File Purpose: Reminder domain models.
Module: app.models.reminder
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: dataclasses, typing.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class WorkReminder:
    """Reminder-ready work item summary."""

    work_item_id: int
    title: str
    client_name: str
    assigned_to_name: str
    status: str
    due_date: str
    reminder_type: str
    days_delta: int


@dataclass(frozen=True)
class ReminderSummary:
    """Reminder summary for the current user."""

    overdue_count: int
    upcoming_count: int
    reminders: tuple[WorkReminder, ...]
