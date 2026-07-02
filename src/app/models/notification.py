"""
File Purpose: Notification queue domain models.
Module: app.models.notification
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: dataclasses, typing.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class NotificationRecord:
    """Queued notification record."""

    id: int
    recipient_user_id: int
    recipient_name: str
    related_work_item_id: Optional[int]
    notification_type: str
    provider: str
    message: str
    status: str
    failure_reason: Optional[str]
    retry_count: int
    sent_at: Optional[str]
    created_at: str


@dataclass(frozen=True)
class NotificationInput:
    """Input data for queueing a notification."""

    recipient_user_id: int
    notification_type: str
    message: str
    provider: str = "manual"
    related_work_item_id: Optional[int] = None
