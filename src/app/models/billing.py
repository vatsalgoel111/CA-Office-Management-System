"""
File Purpose: Billing domain models.
Module: app.models.billing
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: dataclasses, typing.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Bill:
    """Client bill record."""

    id: int
    client_id: int
    client_name: str
    work_item_id: Optional[int]
    work_title: Optional[str]
    bill_number: str
    bill_date: str
    amount_paise: int
    status: str

    @property
    def amount_rupees(self) -> str:
        """Return bill amount formatted in rupees."""

        return f"Rs. {self.amount_paise / 100:,.2f}"


@dataclass(frozen=True)
class BillInput:
    """Input data for creating bills."""

    client_id: int
    bill_number: str
    bill_date: str
    amount_rupees: str
    work_item_id: Optional[int] = None
