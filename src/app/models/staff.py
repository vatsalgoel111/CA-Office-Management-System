"""
File Purpose: Staff management input models.
Module: app.models.staff
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: dataclasses.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class StaffInput:
    """Input data for creating staff user accounts."""

    full_name: str
    username: str
    password: str
    role_code: str = "staff"
    mobile: str = ""
    email: str = ""
