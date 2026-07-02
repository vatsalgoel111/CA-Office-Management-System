"""
File Purpose: Reminder view using reusable UI components.
Module: app.ui.reminder_view
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: customtkinter, app.controllers.reminder_controller, app.ui.
"""

import customtkinter as ctk

from app.controllers.reminder_controller import ReminderController
from app.ui.components import DataTable, InfoCard, SecondaryButton
from app.ui.theme import theme_manager


class ReminderView(ctk.CTkFrame):
    """Overdue and upcoming work reminders."""

    COLUMNS = ("Type", "Due Date", "Client", "Work", "Assigned To", "Status", "Days")

    def __init__(self, master, controller: ReminderController, **kwargs) -> None:
        super().__init__(master, fg_color=theme_manager.color("bg"), **kwargs)
        self._controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self._build()
        self._refresh()

    def _build(self) -> None:
        ctk.CTkLabel(
            self,
            text="Reminders",
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.page, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(24, 8))
        ctk.CTkLabel(
            self,
            text="Track overdue and upcoming work due dates.",
            text_color=theme_manager.color("text_muted"),
            font=theme_manager.font(theme_manager.tokens.fonts.body),
        ).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 16))

        self.cards = ctk.CTkFrame(self, fg_color="transparent")
        self.cards.grid(row=2, column=0, sticky="ew", padx=24, pady=(0, 16))
        self.cards.grid_columnconfigure((0, 1), weight=1)

        SecondaryButton(self, "Refresh", command=self._refresh).grid(
            row=3,
            column=0,
            sticky="e",
            padx=24,
            pady=(0, 12),
        )

        self.table = DataTable(self, self.COLUMNS)
        self.table.grid(row=4, column=0, sticky="nsew", padx=24, pady=(0, 24))

    def _refresh(self) -> None:
        for child in self.cards.winfo_children():
            child.destroy()
        summary = self._controller.get_summary()
        InfoCard(self.cards, "Overdue", str(summary.overdue_count), "Past due work").grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 8),
        )
        InfoCard(self.cards, "Upcoming", str(summary.upcoming_count), "Due within 7 days").grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(8, 0),
        )
        self.table.set_rows(
            (
                reminder.reminder_type.title(),
                reminder.due_date,
                reminder.client_name,
                reminder.title,
                reminder.assigned_to_name,
                reminder.status.replace("_", " ").title(),
                str(reminder.days_delta),
            )
            for reminder in summary.reminders
        )
