"""
File Purpose: Authenticated application shell view.
Module: app.ui.app_shell
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: customtkinter, app.constants, app.models.session, app.ui.
"""

import customtkinter as ctk

from app.constants import PermissionCode
from app.models.session import UserSession
from app.ui.dashboard_placeholder import DashboardPlaceholder
from app.ui.navigation import NavigationItem, NavigationShell
from app.ui.theme import theme_manager


class AppShell(ctk.CTkFrame):
    """Authenticated application shell with permission-aware navigation."""

    NAVIGATION_ITEMS = (
        NavigationItem("dashboard", "Dashboard"),
        NavigationItem("clients", "Clients", PermissionCode.CLIENTS_VIEW.value),
        NavigationItem("work", "Work", PermissionCode.WORK_VIEW_ASSIGNED.value),
        NavigationItem("reports", "Reports", PermissionCode.REPORTS_VIEW.value),
    )

    def __init__(self, master, session: UserSession, **kwargs) -> None:
        super().__init__(master, fg_color=theme_manager.color("bg"), **kwargs)
        self.session = session
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.shell = NavigationShell(
            self,
            title="Dashboard",
            items=self.NAVIGATION_ITEMS,
            user_permissions=session.permissions,
            on_navigate=self.show_route,
            active_key="dashboard",
        )
        self.shell.grid(row=0, column=0, sticky="nsew")
        self.show_route("dashboard")

    def show_route(self, route_key: str) -> None:
        """Show a route inside the authenticated shell."""

        for child in self.shell.content.winfo_children():
            child.destroy()

        if route_key == "dashboard":
            DashboardPlaceholder(self.shell.content, self.session).pack(
                fill="both",
                expand=True,
            )
            return

        ctk.CTkLabel(
            self.shell.content,
            text=f"{route_key.title()} module is not implemented yet.",
            text_color=theme_manager.color("text_muted"),
            font=theme_manager.font(theme_manager.tokens.fonts.section, "bold"),
        ).pack(padx=24, pady=24, anchor="w")

