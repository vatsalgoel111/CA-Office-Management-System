"""
File Purpose: Authenticated application shell view.
Module: app.ui.app_shell
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: customtkinter, app.constants, app.controllers, app.models.session, app.repositories, app.services, app.ui.
"""

import customtkinter as ctk

from app.constants import PermissionCode
from app.controllers.dashboard_controller import DashboardController
from app.models.session import UserSession
from app.repositories.dashboard_repository import DashboardRepository
from app.services.dashboard_service import DashboardService
from app.database.connection import DatabaseConnectionManager
from app.ui.dashboard_view import DashboardView
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

    def __init__(
        self,
        master,
        session: UserSession,
        database: DatabaseConnectionManager,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color=theme_manager.color("bg"), **kwargs)
        self.session = session
        self.dashboard_controller = DashboardController(
            DashboardService(DashboardRepository(database)),
            session,
        )
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
            DashboardView(self.shell.content, self.dashboard_controller).pack(
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
