"""
File Purpose: Work management domain models.
Module: app.models.work
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: dataclasses, typing.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class WorkItem:
    """Assigned office work item."""

    id: int
    client_id: int
    client_name: str
    assigned_to_user_id: int
    assigned_to_name: str
    assigned_by_user_id: int
    work_type: str
    title: str
    description: Optional[str]
    priority: str
    status: str
    due_date: Optional[str]
    completed_at: Optional[str]


@dataclass(frozen=True)
class WorkAssignmentInput:
    """Input data for assigning work."""

    client_id: int
    assigned_to_user_id: int
    work_type: str
    title: str
    description: str = ""
    priority: str = "normal"
    due_date: str = ""

