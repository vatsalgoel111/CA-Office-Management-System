"""CustomTkinter user interface modules and reusable components."""

from app.ui.components import (
    ConfirmationDialog,
    DataTable,
    FormField,
    IconButton,
    InfoCard,
    LoadingOverlay,
    NotificationToast,
    PrimaryButton,
    SearchBox,
    SecondaryButton,
    Sidebar,
    StatusBadge,
    TopBar,
)
from app.ui.app_shell import AppShell
from app.ui.billing_view import BillingView
from app.ui.client_view import ClientView
from app.ui.collection_view import CollectionView
from app.ui.dashboard_view import DashboardView
from app.ui.login_view import LoginView
from app.ui.navigation import NavigationItem, NavigationShell
from app.ui.report_view import ReportView
from app.ui.staff_view import StaffView
from app.ui.theme import ThemeManager, theme_manager
from app.ui.window_manager import WindowManager
from app.ui.work_view import WorkView

__all__ = [
    "ConfirmationDialog",
    "DataTable",
    "AppShell",
    "BillingView",
    "ClientView",
    "CollectionView",
    "DashboardView",
    "FormField",
    "IconButton",
    "InfoCard",
    "LoadingOverlay",
    "LoginView",
    "NavigationItem",
    "NavigationShell",
    "NotificationToast",
    "PrimaryButton",
    "ReportView",
    "SearchBox",
    "SecondaryButton",
    "Sidebar",
    "StaffView",
    "StatusBadge",
    "ThemeManager",
    "TopBar",
    "WindowManager",
    "WorkView",
    "theme_manager",
]
