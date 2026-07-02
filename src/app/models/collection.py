"""
File Purpose: Collection tracking domain models.
Module: app.models.collection
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: dataclasses.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CollectionRecord:
    """Payment collection record linked to a bill."""

    id: int
    bill_id: int
    bill_number: str
    client_name: str
    received_amount_paise: int
    received_date: str
    payment_mode: str
    notes: str

    @property
    def received_amount_rupees(self) -> str:
        """Return received amount formatted in rupees."""

        return f"Rs. {self.received_amount_paise / 100:,.2f}"


@dataclass(frozen=True)
class CollectionInput:
    """Input data for recording collections."""

    bill_id: int
    received_amount_rupees: str
    received_date: str
    payment_mode: str = "other"
    notes: str = ""
