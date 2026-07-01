"""
File Purpose: Navigation framework primitives for permission-aware UI shells.
Module: app.ui.navigation
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: dataclasses, typing, customtkinter, app.ui.components, app.ui.theme.
"""

from dataclasses import dataclass
from typing import Callable, Iterable, Optional, Sequence, Set

import customtkinter as ctk

from app.ui.components import Sidebar, TopBar
from app.ui.theme import theme_manager


@dataclass(frozen=True)
class NavigationItem:
    """Describes one navigation item."""

    key: str
    label: str
    required_permission: Optional[str] = None


class NavigationShell(ctk.CTkFrame):
    """Reusable shell with sidebar, top bar, and content area."""

    def __init__(
        self,
        master,
        title: str,
        items: Sequence[NavigationItem],
        user_permissions: Iterable[str],
        on_navigate: Callable[[str], None],
        active_key: str = "",
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color=theme_manager.color("bg"), **kwargs)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        permissions: Set[str] = set(user_permissions)
        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.top_bar = TopBar(self, title=title)
        self.top_bar.grid(row=0, column=1, sticky="ew")

        self.content = ctk.CTkFrame(self, fg_color=theme_manager.color("bg"))
        self.content.grid(row=1, column=1, sticky="nsew")

        for item in items:
            if item.required_permission and item.required_permission not in permissions:
                continue
            self.sidebar.add_item(
                item.label,
                command=lambda key=item.key: on_navigate(key),
                active=item.key == active_key,
            )

