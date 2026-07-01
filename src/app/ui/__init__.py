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
from app.ui.dashboard_placeholder import DashboardPlaceholder
from app.ui.login_view import LoginView
from app.ui.navigation import NavigationItem, NavigationShell
from app.ui.theme import ThemeManager, theme_manager
from app.ui.window_manager import WindowManager

__all__ = [
    "ConfirmationDialog",
    "DataTable",
    "AppShell",
    "DashboardPlaceholder",
    "FormField",
    "IconButton",
    "InfoCard",
    "LoadingOverlay",
    "LoginView",
    "NavigationItem",
    "NavigationShell",
    "NotificationToast",
    "PrimaryButton",
    "SearchBox",
    "SecondaryButton",
    "Sidebar",
    "StatusBadge",
    "ThemeManager",
    "TopBar",
    "WindowManager",
    "theme_manager",
]
