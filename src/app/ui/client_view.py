"""
File Purpose: Client management view using reusable UI components.
Module: app.ui.client_view
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: customtkinter, app.controllers.client_controller, app.models.client, app.ui.
"""

from typing import List

import customtkinter as ctk

from app.controllers.client_controller import ClientController
from app.models.client import Client, ClientInput
from app.ui.components import DataTable, FormField, PrimaryButton, SearchBox, SecondaryButton
from app.ui.theme import theme_manager


class ClientView(ctk.CTkFrame):
    """Client list and basic add/deactivate workflow."""

    COLUMNS = ("Name", "Business", "Mobile", "PAN", "GSTIN", "Status")

    def __init__(self, master, controller: ClientController, **kwargs) -> None:
        super().__init__(master, fg_color=theme_manager.color("bg"), **kwargs)
        self._controller = controller
        self._clients: List[Client] = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self._build()
        self._refresh()

    def _build(self) -> None:
        ctk.CTkLabel(
            self,
            text="Clients",
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.page, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(24, 8))

        ctk.CTkLabel(
            self,
            text="Manage client master records. Excel import will be added later.",
            text_color=theme_manager.color("text_muted"),
            font=theme_manager.font(theme_manager.tokens.fonts.body),
        ).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 16))

        self.search_box = SearchBox(self, "Search clients", self._refresh)
        self.search_box.grid(row=2, column=0, sticky="ew", padx=24, pady=(0, 16))

        form = ctk.CTkFrame(
            self,
            fg_color=theme_manager.color("surface"),
            border_color=theme_manager.color("border"),
            border_width=1,
            corner_radius=theme_manager.tokens.radius.lg,
        )
        form.grid(row=3, column=0, sticky="ew", padx=24, pady=(0, 16))
        for column in range(4):
            form.grid_columnconfigure(column, weight=1)

        self.client_name = FormField(form, "Client Name", required=True)
        self.client_name.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        self.business_name = FormField(form, "Business Name")
        self.business_name.grid(row=0, column=1, sticky="ew", padx=12, pady=12)
        self.mobile = FormField(form, "Mobile")
        self.mobile.grid(row=0, column=2, sticky="ew", padx=12, pady=12)
        self.pan = FormField(form, "PAN")
        self.pan.grid(row=0, column=3, sticky="ew", padx=12, pady=12)

        self.message_label = ctk.CTkLabel(
            form,
            text="",
            text_color=theme_manager.color("error"),
            font=theme_manager.font(theme_manager.tokens.fonts.small),
        )
        self.message_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=12)

        actions = ctk.CTkFrame(form, fg_color="transparent")
        actions.grid(row=1, column=2, columnspan=2, sticky="e", padx=12, pady=(0, 12))
        SecondaryButton(actions, "Clear", command=self._clear_form).pack(side="right")
        PrimaryButton(actions, "Add Client", command=self._add_client).pack(
            side="right",
            padx=(0, 8),
        )

        self.table = DataTable(self, self.COLUMNS)
        self.table.grid(row=4, column=0, sticky="nsew", padx=24, pady=(0, 12))

        self.deactivate_button = SecondaryButton(
            self,
            "Deactivate First Listed Client",
            command=self._deactivate_first_client,
        )
        self.deactivate_button.grid(row=5, column=0, sticky="e", padx=24, pady=(0, 24))

    def _refresh(self, search_text: str = "") -> None:
        search = search_text if search_text else self.search_box.get()
        self._clients = self._controller.search(search)
        self.table.set_rows(
            (
                client.client_name,
                client.business_name or "",
                client.mobile or "",
                client.pan or "",
                client.gstin or "",
                client.status.title(),
            )
            for client in self._clients
        )

    def _add_client(self) -> None:
        self.message_label.configure(text="")
        error = self._controller.create(
            ClientInput(
                client_name=self.client_name.get(),
                business_name=self.business_name.get(),
                mobile=self.mobile.get(),
                pan=self.pan.get(),
            )
        )
        if error:
            self.message_label.configure(text=error)
            return
        self._clear_form()
        self._refresh()

    def _deactivate_first_client(self) -> None:
        if not self._clients:
            self.message_label.configure(text="No active client selected")
            return
        error = self._controller.deactivate(self._clients[0].id)
        if error:
            self.message_label.configure(text=error)
            return
        self._refresh()

    def _clear_form(self) -> None:
        for field in (self.client_name, self.business_name, self.mobile, self.pan):
            field.input.delete(0, "end")
            field.clear_error()
        self.message_label.configure(text="")

