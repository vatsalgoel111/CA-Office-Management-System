"""
File Purpose: Dashboard view using reusable dashboard components.
Module: app.ui.dashboard_view
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: customtkinter, app.controllers.dashboard_controller, app.ui.components.
"""

import customtkinter as ctk

from app.controllers.dashboard_controller import DashboardController
from app.ui.components import InfoCard
from app.ui.theme import theme_manager


class DashboardView(ctk.CTkFrame):
    """Authenticated dashboard summary view."""

    def __init__(self, master, controller: DashboardController, **kwargs) -> None:
        super().__init__(master, fg_color=theme_manager.color("bg"), **kwargs)
        self._controller = controller
        self.grid_columnconfigure(0, weight=1)
        self._build()

    def _build(self) -> None:
        summary = self._controller.get_summary()

        ctk.CTkLabel(
            self,
            text="Dashboard",
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.page, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(24, 8))

        ctk.CTkLabel(
            self,
            text="Office summary for current work and collections.",
            text_color=theme_manager.color("text_muted"),
            font=theme_manager.font(theme_manager.tokens.fonts.body),
        ).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 24))

        cards = ctk.CTkFrame(self, fg_color="transparent")
        cards.grid(row=2, column=0, sticky="ew", padx=24)
        for column in range(3):
            cards.grid_columnconfigure(column, weight=1)

        card_data = (
            ("Active Clients", str(summary.active_clients), "Currently active"),
            ("Pending Work", str(summary.pending_work), "Open work items"),
            ("Overdue Work", str(summary.overdue_work), "Needs attention"),
            ("Completed Work", str(summary.completed_work), "Finished tasks"),
            ("Unpaid Bills", str(summary.unpaid_bills), "Unpaid or partial"),
            ("Outstanding", summary.outstanding_amount_rupees, "Total balance"),
        )

        for index, (title, value, subtitle) in enumerate(card_data):
            row = index // 3
            column = index % 3
            InfoCard(cards, title, value, subtitle).grid(
                row=row,
                column=column,
                sticky="ew",
                padx=(0 if column == 0 else 12, 0 if column == 2 else 12),
                pady=(0, 24),
            )

