"""
File Purpose: Work management view using reusable UI components.
Module: app.ui.work_view
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, customtkinter, app.controllers, app.models.work, app.ui.
"""

from typing import List

import customtkinter as ctk

from app.controllers.work_controller import WorkController
from app.controllers.lookup_controller import LookupController
from app.models.work import WorkAssignmentInput, WorkItem
from app.ui.components import (
    DataTable,
    DatePickerField,
    FormField,
    PrimaryButton,
    SearchableDropdown,
    SecondaryButton,
)
from app.ui.theme import theme_manager


class WorkView(ctk.CTkFrame):
    """Work list, assignment, and status foundation view."""

    COLUMNS = ("Title", "Client", "Assigned To", "Type", "Priority", "Status", "Due")

    def __init__(
        self,
        master,
        controller: WorkController,
        lookup_controller: LookupController,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color=theme_manager.color("bg"), **kwargs)
        self._controller = controller
        self._lookup_controller = lookup_controller
        self._work_items: List[WorkItem] = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self._build()
        self._refresh()

    def _build(self) -> None:
        ctk.CTkLabel(
            self,
            text="Work",
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.page, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(24, 8))

        ctk.CTkLabel(
            self,
            text="Assign work and update visible task status.",
            text_color=theme_manager.color("text_muted"),
            font=theme_manager.font(theme_manager.tokens.fonts.body),
        ).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 16))

        form = ctk.CTkFrame(
            self,
            fg_color=theme_manager.color("surface"),
            border_color=theme_manager.color("border"),
            border_width=1,
            corner_radius=theme_manager.tokens.radius.lg,
        )
        form.grid(row=2, column=0, sticky="ew", padx=24, pady=(0, 16))
        for column in range(5):
            form.grid_columnconfigure(column, weight=1)

        self.client = SearchableDropdown(form, "Client", required=True)
        self.client.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        self.assigned_to_user = SearchableDropdown(form, "Assigned To", required=True)
        self.assigned_to_user.grid(row=0, column=1, sticky="ew", padx=12, pady=12)
        self.work_type = FormField(form, "Work Type", required=True)
        self.work_type.grid(row=0, column=2, sticky="ew", padx=12, pady=12)
        self.title = FormField(form, "Title", required=True)
        self.title.grid(row=0, column=3, sticky="ew", padx=12, pady=12)
        self.due_date = DatePickerField(form, "Due Date")
        self.due_date.grid(row=0, column=4, sticky="ew", padx=12, pady=12)

        self.message_label = ctk.CTkLabel(
            form,
            text="",
            text_color=theme_manager.color("error"),
            font=theme_manager.font(theme_manager.tokens.fonts.small),
        )
        self.message_label.grid(row=1, column=0, columnspan=3, sticky="w", padx=12)

        actions = ctk.CTkFrame(form, fg_color="transparent")
        actions.grid(row=1, column=3, columnspan=2, sticky="e", padx=12, pady=(0, 12))
        SecondaryButton(actions, "Refresh", command=self._refresh).pack(side="right")
        PrimaryButton(actions, "Assign Work", command=self._assign_work).pack(
            side="right",
            padx=(0, 8),
        )

        self.table = DataTable(self, self.COLUMNS, empty_message="No work items found.")
        self.table.grid(row=4, column=0, sticky="nsew", padx=24, pady=(0, 12))

        bottom_actions = ctk.CTkFrame(self, fg_color="transparent")
        bottom_actions.grid(row=5, column=0, sticky="e", padx=24, pady=(0, 24))
        SecondaryButton(
            bottom_actions,
            "Mark First Listed Completed",
            command=self._complete_first_item,
        ).pack(side="right")

    def _refresh(self) -> None:
        self.client.set_choices(self._lookup_controller.active_clients())
        self.assigned_to_user.set_choices(self._lookup_controller.active_users())
        self._work_items = self._controller.list_work()
        self.table.set_rows(
            (
                item.title,
                item.client_name,
                item.assigned_to_name,
                item.work_type,
                item.priority.title(),
                item.status.replace("_", " ").title(),
                item.due_date or "",
            )
            for item in self._work_items
        )

    def _assign_work(self) -> None:
        self.message_label.configure(text="")
        client_id = self.client.get_selected_id()
        assigned_user_id = self.assigned_to_user.get_selected_id()
        if client_id is None or assigned_user_id is None:
            self.message_label.configure(text="Select a client and assigned staff member.")
            return

        error = self._controller.assign(
            WorkAssignmentInput(
                client_id=client_id,
                assigned_to_user_id=assigned_user_id,
                work_type=self.work_type.get(),
                title=self.title.get(),
                due_date=self.due_date.get(),
            )
        )
        if error:
            self.message_label.configure(text=error)
            return
        self._clear_form()
        self._refresh()

    def _complete_first_item(self) -> None:
        if not self._work_items:
            self.message_label.configure(text="No visible work item selected")
            return
        error = self._controller.update_status(
            self._work_items[0].id,
            "completed",
            "Marked completed from work screen.",
        )
        if error:
            self.message_label.configure(text=error)
            return
        self._refresh()

    def _clear_form(self) -> None:
        for field in (
            self.client,
            self.assigned_to_user,
            self.work_type,
            self.title,
            self.due_date,
        ):
            if hasattr(field, "input"):
                field.input.delete(0, "end")
            else:
                field.clear()
            field.clear_error()
        self.message_label.configure(text="")
