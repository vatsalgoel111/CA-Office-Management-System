"""
File Purpose: Staff management view using reusable UI components.
Module: app.ui.staff_view
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, customtkinter, app.controllers.staff_controller, app.models, app.ui.
"""

from typing import List

import customtkinter as ctk

from app.controllers.staff_controller import StaffController
from app.models.staff import StaffInput
from app.models.user import User
from app.ui.components import DataTable, FormField, PrimaryButton, SearchBox, SecondaryButton
from app.ui.theme import theme_manager


class StaffView(ctk.CTkFrame):
    """Staff list and account creation workflow."""

    COLUMNS = ("Name", "Username", "Role", "Mobile", "Email", "Status")

    def __init__(self, master, controller: StaffController, **kwargs) -> None:
        super().__init__(master, fg_color=theme_manager.color("bg"), **kwargs)
        self._controller = controller
        self._staff: List[User] = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self._build()
        self._refresh()

    def _build(self) -> None:
        ctk.CTkLabel(
            self,
            text="Staff",
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.page, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(24, 8))

        ctk.CTkLabel(
            self,
            text="Manage staff accounts and role assignment.",
            text_color=theme_manager.color("text_muted"),
            font=theme_manager.font(theme_manager.tokens.fonts.body),
        ).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 16))

        self.search_box = SearchBox(self, "Search staff", self._refresh)
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

        self.full_name = FormField(form, "Full Name", required=True)
        self.full_name.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        self.username = FormField(form, "Username", required=True)
        self.username.grid(row=0, column=1, sticky="ew", padx=12, pady=12)
        self.password = FormField(form, "Password", required=True)
        self.password.grid(row=0, column=2, sticky="ew", padx=12, pady=12)
        self.role_code = FormField(form, "Role Code", required=True, placeholder="staff")
        self.role_code.grid(row=0, column=3, sticky="ew", padx=12, pady=12)
        self.mobile = FormField(form, "Mobile")
        self.mobile.grid(row=0, column=4, sticky="ew", padx=12, pady=12)

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
        PrimaryButton(actions, "Add Staff", command=self._add_staff).pack(
            side="right",
            padx=(0, 8),
        )

        self.table = DataTable(self, self.COLUMNS)
        self.table.grid(row=4, column=0, sticky="nsew", padx=24, pady=(0, 12))

        bottom_actions = ctk.CTkFrame(self, fg_color="transparent")
        bottom_actions.grid(row=5, column=0, sticky="e", padx=24, pady=(0, 24))
        SecondaryButton(
            bottom_actions,
            "Activate First Listed",
            command=self._activate_first_staff,
        ).pack(side="right")
        SecondaryButton(
            bottom_actions,
            "Deactivate First Listed",
            command=self._deactivate_first_staff,
        ).pack(side="right", padx=(0, 8))

    def _refresh(self, search_text: str = "") -> None:
        search = search_text if search_text else self.search_box.get()
        self._staff = self._controller.list_staff(search)
        self.table.set_rows(
            (
                user.full_name,
                user.username,
                user.role_name,
                user.mobile or "",
                user.email or "",
                "Active" if user.is_active else "Inactive",
            )
            for user in self._staff
        )

    def _add_staff(self) -> None:
        self.message_label.configure(text="")
        error = self._controller.create(
            StaffInput(
                full_name=self.full_name.get(),
                username=self.username.get(),
                password=self.password.get(),
                role_code=self.role_code.get() or "staff",
                mobile=self.mobile.get(),
            )
        )
        if error:
            self.message_label.configure(text=error)
            return
        self._clear_form()
        self._refresh()

    def _activate_first_staff(self) -> None:
        if not self._staff:
            self.message_label.configure(text="No staff account selected")
            return
        error = self._controller.activate(self._staff[0].id)
        if error:
            self.message_label.configure(text=error)
            return
        self._refresh()

    def _deactivate_first_staff(self) -> None:
        if not self._staff:
            self.message_label.configure(text="No staff account selected")
            return
        error = self._controller.deactivate(self._staff[0].id)
        if error:
            self.message_label.configure(text=error)
            return
        self._refresh()

    def _clear_form(self) -> None:
        for field in (
            self.full_name,
            self.username,
            self.password,
            self.role_code,
            self.mobile,
        ):
            field.input.delete(0, "end")
            field.clear_error()
        self.message_label.configure(text="")
