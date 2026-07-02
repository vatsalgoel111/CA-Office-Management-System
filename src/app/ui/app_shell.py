"""
File Purpose: Authenticated application shell view.
Module: app.ui.app_shell
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: customtkinter, app.constants, app.controllers, app.database, app.models.session, app.repositories, app.services, app.ui.
"""

import customtkinter as ctk

from app.constants import PermissionCode
from app.controllers.billing_controller import BillingController
from app.controllers.client_controller import ClientController
from app.controllers.collection_controller import CollectionController
from app.controllers.dashboard_controller import DashboardController
from app.controllers.report_controller import ReportController
from app.controllers.staff_controller import StaffController
from app.controllers.work_controller import WorkController
from app.database.connection import DatabaseConnectionManager
from app.core.paths import AppPaths
from app.models.session import UserSession
from app.repositories.client_repository import ClientRepository
from app.repositories.billing_repository import BillingRepository
from app.repositories.collection_repository import CollectionRepository
from app.repositories.dashboard_repository import DashboardRepository
from app.repositories.report_repository import ReportRepository
from app.repositories.user_repository import UserRepository
from app.repositories.work_repository import WorkRepository
from app.services.billing_service import BillingService
from app.services.client_service import ClientService
from app.services.collection_service import CollectionService
from app.services.dashboard_service import DashboardService
from app.services.report_service import ReportService
from app.services.staff_service import StaffService
from app.services.work_service import WorkService
from app.ui.billing_view import BillingView
from app.ui.client_view import ClientView
from app.ui.collection_view import CollectionView
from app.ui.dashboard_view import DashboardView
from app.ui.navigation import NavigationItem, NavigationShell
from app.ui.report_view import ReportView
from app.ui.staff_view import StaffView
from app.ui.theme import theme_manager
from app.ui.work_view import WorkView


class AppShell(ctk.CTkFrame):
    """Authenticated application shell with permission-aware navigation."""

    NAVIGATION_ITEMS = (
        NavigationItem("dashboard", "Dashboard"),
        NavigationItem("clients", "Clients", PermissionCode.CLIENTS_VIEW.value),
        NavigationItem("staff", "Staff", PermissionCode.USERS_MANAGE.value),
        NavigationItem(
            "work",
            "Work",
            (
                PermissionCode.WORK_VIEW_ALL.value,
                PermissionCode.WORK_VIEW_ASSIGNED.value,
            ),
        ),
        NavigationItem("billing", "Billing", PermissionCode.BILLING_MANAGE.value),
        NavigationItem(
            "collections",
            "Collections",
            PermissionCode.COLLECTIONS_MANAGE.value,
        ),
        NavigationItem("reports", "Reports", PermissionCode.REPORTS_VIEW.value),
    )

    def __init__(
        self,
        master,
        session: UserSession,
        database: DatabaseConnectionManager,
        paths: AppPaths,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color=theme_manager.color("bg"), **kwargs)
        self.session = session
        self.dashboard_controller = DashboardController(
            DashboardService(DashboardRepository(database)),
            session,
        )
        self.client_controller = ClientController(
            ClientService(ClientRepository(database)),
            session,
        )
        self.staff_controller = StaffController(
            StaffService(UserRepository(database)),
            session,
        )
        self.work_controller = WorkController(
            WorkService(WorkRepository(database)),
            session,
        )
        self.billing_controller = BillingController(
            BillingService(BillingRepository(database)),
            session,
        )
        self.collection_controller = CollectionController(
            CollectionService(CollectionRepository(database)),
            session,
        )
        self.report_controller = ReportController(
            ReportService(ReportRepository(database), paths),
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

        if route_key == "clients":
            ClientView(self.shell.content, self.client_controller).pack(
                fill="both",
                expand=True,
            )
            return

        if route_key == "staff":
            StaffView(self.shell.content, self.staff_controller).pack(
                fill="both",
                expand=True,
            )
            return

        if route_key == "work":
            WorkView(self.shell.content, self.work_controller).pack(
                fill="both",
                expand=True,
            )
            return

        if route_key == "billing":
            BillingView(self.shell.content, self.billing_controller).pack(
                fill="both",
                expand=True,
            )
            return

        if route_key == "collections":
            CollectionView(self.shell.content, self.collection_controller).pack(
                fill="both",
                expand=True,
            )
            return

        if route_key == "reports":
            ReportView(self.shell.content, self.report_controller).pack(
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
