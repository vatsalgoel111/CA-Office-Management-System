"""
File Purpose: Collection tracking view using reusable UI components.
Module: app.ui.collection_view
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, customtkinter, app.controllers, app.models, app.ui.
"""

from typing import List

import customtkinter as ctk

from app.controllers.collection_controller import CollectionController
from app.controllers.lookup_controller import LookupController
from app.models.collection import CollectionInput, CollectionRecord
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


class CollectionView(ctk.CTkFrame):
    """Collection list and payment entry foundation view."""

    COLUMNS = ("Bill No", "Client", "Date", "Amount", "Mode", "Notes")

    def __init__(
        self,
        master,
        controller: CollectionController,
        lookup_controller: LookupController,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color=theme_manager.color("bg"), **kwargs)
        self._controller = controller
        self._lookup_controller = lookup_controller
        self._collections: List[CollectionRecord] = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self._build()
        self._refresh()

    def _build(self) -> None:
        ctk.CTkLabel(
            self,
            text="Collections",
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.page, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(24, 8))

        ctk.CTkLabel(
            self,
            text="Record client payments and update bill status automatically.",
            text_color=theme_manager.color("text_muted"),
            font=theme_manager.font(theme_manager.tokens.fonts.body),
        ).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 16))

        self.search_box = SearchBox(self, "Search collections", self._refresh)
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

        self.bill = SearchableDropdown(form, "Bill", required=True)
        self.bill.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        self.amount = FormField(form, "Amount", required=True, placeholder="1000.00")
        self.amount.grid(row=0, column=1, sticky="ew", padx=12, pady=12)
        self.received_date = DatePickerField(form, "Received Date", required=True)
        self.received_date.grid(row=0, column=2, sticky="ew", padx=12, pady=12)
        self.payment_mode = FormField(form, "Payment Mode", placeholder="bank")
        self.payment_mode.grid(row=0, column=3, sticky="ew", padx=12, pady=12)
        self.notes = FormField(form, "Notes")
        self.notes.grid(row=0, column=4, sticky="ew", padx=12, pady=12)

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
        PrimaryButton(actions, "Record Collection", command=self._record_collection).pack(
            side="right",
            padx=(0, 8),
        )

        self.table = DataTable(self, self.COLUMNS, empty_message="No collections found.")
        self.table.grid(row=4, column=0, sticky="nsew", padx=24, pady=(0, 24))

    def _refresh(self, search_text: str = "") -> None:
        self.bill.set_choices(self._lookup_controller.open_bills())
        search = search_text if search_text else self.search_box.get()
        self._collections = self._controller.list_collections(search)
        self.table.set_rows(
            (
                collection.bill_number,
                collection.client_name,
                collection.received_date,
                collection.received_amount_rupees,
                collection.payment_mode.title(),
                collection.notes,
            )
            for collection in self._collections
        )

    def _record_collection(self) -> None:
        self.message_label.configure(text="")
        bill_id = self.bill.get_selected_id()
        if bill_id is None:
            self.message_label.configure(text="Select an unpaid or partially paid bill.")
            return

        error = self._controller.record(
            CollectionInput(
                bill_id=bill_id,
                received_amount_rupees=self.amount.get(),
                received_date=self.received_date.get(),
                payment_mode=self.payment_mode.get() or "other",
                notes=self.notes.get(),
            )
        )
        if error:
            self.message_label.configure(text=error)
            return
        self._clear_form()
        self._refresh()

    def _clear_form(self) -> None:
        for field in (
            self.bill,
            self.amount,
            self.received_date,
            self.payment_mode,
            self.notes,
        ):
            if hasattr(field, "input"):
                field.input.delete(0, "end")
            else:
                field.clear()
            field.clear_error()
        self.message_label.configure(text="")
