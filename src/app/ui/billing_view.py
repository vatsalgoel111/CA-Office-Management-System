"""
File Purpose: Billing management view using reusable UI components.
Module: app.ui.billing_view
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, customtkinter, app.controllers, app.models, app.ui.
"""

from typing import List

import customtkinter as ctk

from app.controllers.billing_controller import BillingController
from app.controllers.lookup_controller import LookupController
from app.models.billing import Bill, BillInput
from app.ui.components import (
    DataTable,
    DatePickerField,
    FormField,
    PrimaryButton,
    SearchableDropdown,
    SearchBox,
    SecondaryButton,
)
from app.ui.theme import theme_manager


class BillingView(ctk.CTkFrame):
    """Bill list, creation, and status foundation view."""

    COLUMNS = ("Bill No", "Client", "Date", "Amount", "Status", "Work")

    def __init__(
        self,
        master,
        controller: BillingController,
        lookup_controller: LookupController,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color=theme_manager.color("bg"), **kwargs)
        self._controller = controller
        self._lookup_controller = lookup_controller
        self._bills: List[Bill] = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self._build()
        self._refresh()

    def _build(self) -> None:
        ctk.CTkLabel(
            self,
            text="Billing",
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.page, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(24, 8))

        ctk.CTkLabel(
            self,
            text="Create bills and track billing status. Collections will be added next.",
            text_color=theme_manager.color("text_muted"),
            font=theme_manager.font(theme_manager.tokens.fonts.body),
        ).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 16))

        self.search_box = SearchBox(self, "Search bills", self._refresh)
        self.search_box.grid(row=2, column=0, sticky="ew", padx=24, pady=(0, 16))

        form = ctk.CTkFrame(
            self,
            fg_color=theme_manager.color("surface"),
            border_color=theme_manager.color("border"),
            border_width=1,
            corner_radius=theme_manager.tokens.radius.lg,
        )
        form.grid(row=3, column=0, sticky="ew", padx=24, pady=(0, 16))
        for column in range(5):
            form.grid_columnconfigure(column, weight=1)

        self.client = SearchableDropdown(form, "Client", required=True)
        self.client.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        self.bill_number = FormField(form, "Bill Number", required=True)
        self.bill_number.grid(row=0, column=1, sticky="ew", padx=12, pady=12)
        self.bill_date = DatePickerField(form, "Bill Date", required=True)
        self.bill_date.grid(row=0, column=2, sticky="ew", padx=12, pady=12)
        self.amount = FormField(form, "Amount", required=True, placeholder="1000.00")
        self.amount.grid(row=0, column=3, sticky="ew", padx=12, pady=12)
        self.work_item = SearchableDropdown(form, "Related Work")
        self.work_item.grid(row=0, column=4, sticky="ew", padx=12, pady=12)

        self.message_label = ctk.CTkLabel(
            form,
            text="",
            text_color=theme_manager.color("error"),
            font=theme_manager.font(theme_manager.tokens.fonts.small),
        )
        self.message_label.grid(row=1, column=0, columnspan=3, sticky="w", padx=12)

        actions = ctk.CTkFrame(form, fg_color="transparent")
        actions.grid(row=1, column=3, columnspan=2, sticky="e", padx=12, pady=(0, 12))
        SecondaryButton(actions, "Clear", command=self._clear_form).pack(side="right")
        PrimaryButton(actions, "Create Bill", command=self._create_bill).pack(
            side="right",
            padx=(0, 8),
        )

        self.table = DataTable(self, self.COLUMNS, empty_message="No bills found.")
        self.table.grid(row=4, column=0, sticky="nsew", padx=24, pady=(0, 12))

        bottom_actions = ctk.CTkFrame(self, fg_color="transparent")
        bottom_actions.grid(row=5, column=0, sticky="e", padx=24, pady=(0, 24))
        SecondaryButton(
            bottom_actions,
            "Mark First Listed Paid",
            command=self._mark_first_paid,
        ).pack(side="right")

    def _refresh(self, search_text: str = "") -> None:
        self.client.set_choices(self._lookup_controller.active_clients())
        self.work_item.set_choices(self._lookup_controller.work_items())
        search = search_text if search_text else self.search_box.get()
        self._bills = self._controller.list_bills(search)
        self.table.set_rows(
            (
                bill.bill_number,
                bill.client_name,
                bill.bill_date,
                bill.amount_rupees,
                bill.status.title(),
                bill.work_title or "",
            )
            for bill in self._bills
        )

    def _create_bill(self) -> None:
        self.message_label.configure(text="")
        client_id = self.client.get_selected_id()
        work_item_id = self.work_item.get_selected_id()
        if client_id is None:
            self.message_label.configure(text="Select a client before creating a bill.")
            return

        error = self._controller.create(
            BillInput(
                client_id=client_id,
                bill_number=self.bill_number.get(),
                bill_date=self.bill_date.get(),
                amount_rupees=self.amount.get(),
                work_item_id=work_item_id,
            )
        )
        if error:
            self.message_label.configure(text=error)
            return
        self._clear_form()
        self._refresh()

    def _mark_first_paid(self) -> None:
        if not self._bills:
            self.message_label.configure(text="No bill selected")
            return
        error = self._controller.update_status(self._bills[0].id, "paid")
        if error:
            self.message_label.configure(text=error)
            return
        self._refresh()

    def _clear_form(self) -> None:
        for field in (
            self.client,
            self.bill_number,
            self.bill_date,
            self.amount,
            self.work_item,
        ):
            if hasattr(field, "input"):
                field.input.delete(0, "end")
            else:
                field.clear()
            field.clear_error()
        self.message_label.configure(text="")
