"""
File Purpose: Client domain models.
Module: app.models.client
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: dataclasses, typing.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Client:
    """Client master record."""

    id: int
    client_name: str
    business_name: Optional[str]
    mobile: Optional[str]
    email: Optional[str]
    pan: Optional[str]
    gstin: Optional[str]
    address: Optional[str]
    client_type: Optional[str]
    status: str
    notes: Optional[str]


@dataclass(frozen=True)
class ClientInput:
    """Input data for creating or updating clients."""

    client_name: str
    business_name: str = ""
    mobile: str = ""
    email: str = ""
    pan: str = ""
    gstin: str = ""
    address: str = ""
    client_type: str = ""
    notes: str = ""

