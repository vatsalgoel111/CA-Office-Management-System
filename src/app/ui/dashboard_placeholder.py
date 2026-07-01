"""
File Purpose: Placeholder dashboard content for authenticated shell routing.
Module: app.ui.dashboard_placeholder
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: customtkinter, app.models.session, app.ui.components, app.ui.theme.
"""

import customtkinter as ctk

from app.models.session import UserSession
from app.ui.components import InfoCard
from app.ui.theme import theme_manager


class DashboardPlaceholder(ctk.CTkFrame):
    """Minimal authenticated dashboard placeholder."""

    def __init__(self, master, session: UserSession, **kwargs) -> None:
        super().__init__(master, fg_color=theme_manager.color("bg"), **kwargs)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text=f"Welcome, {session.user.full_name}",
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.page, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(24, 8))

        ctk.CTkLabel(
            self,
            text="Dashboard metrics will be added in the dashboard module.",
            text_color=theme_manager.color("text_muted"),
            font=theme_manager.font(theme_manager.tokens.fonts.body),
        ).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 24))

        cards = ctk.CTkFrame(self, fg_color="transparent")
        cards.grid(row=2, column=0, sticky="ew", padx=24)
        cards.grid_columnconfigure((0, 1, 2), weight=1)

        InfoCard(
            cards,
            "Current Role",
            session.user.role_name,
            "Resolved after login",
        ).grid(row=0, column=0, sticky="ew", padx=(0, 12))
        InfoCard(
            cards,
            "Permissions",
            str(len(session.permissions)),
            "Loaded from RBAC tables",
        ).grid(row=0, column=1, sticky="ew", padx=12)
        InfoCard(
            cards,
            "Status",
            "Ready",
            "App shell routing active",
        ).grid(row=0, column=2, sticky="ew", padx=(12, 0))

