"""
File Purpose: User and role-related domain models.
Module: app.models.user
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: dataclasses, typing.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class User:
    """Authenticated application user."""

    id: int
    full_name: str
    username: str
    password_hash: str
    role_id: int
    role_code: str
    role_name: str
    mobile: Optional[str]
    email: Optional[str]
    is_active: bool


@dataclass(frozen=True)
class CreateUserRequest:
    """Data needed to create a user."""

    full_name: str
    username: str
    password_hash: str
    role_code: str
    mobile: Optional[str] = None
    email: Optional[str] = None
    is_active: bool = True


@dataclass(frozen=True)
class UpdateUserRequest:
    """Data needed to update a user profile."""

    full_name: str
    role_code: str
    mobile: Optional[str] = None
    email: Optional[str] = None
