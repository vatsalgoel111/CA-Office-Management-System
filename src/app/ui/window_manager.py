"""
File Purpose: Root window and view lifecycle management.
Module: app.ui.window_manager
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, customtkinter, app.constants, app.startup, app.ui.theme.
"""

from typing import Callable, Dict, Optional

import customtkinter as ctk

from app.constants import APP_NAME
from app.startup import ApplicationContext
from app.ui.theme import theme_manager


ViewFactory = Callable[[ctk.CTkFrame, ApplicationContext], ctk.CTkFrame]


class WindowManager:
    """Manages the root application window and registered views."""

    def __init__(self, context: ApplicationContext) -> None:
        self.context = context
        theme_manager.apply("dark")
        self.root = ctk.CTk()
        self.root.title(APP_NAME)
        self.root.geometry("1280x760")
        self.root.minsize(1024, 640)
        self.root.configure(fg_color=theme_manager.color("bg"))
        self._view_factories: Dict[str, ViewFactory] = {}
        self._current_view: Optional[ctk.CTkFrame] = None

    def register_view(self, name: str, factory: ViewFactory) -> None:
        """Register a lazily-created view factory."""

        self._view_factories[name] = factory

    def show_view(self, name: str) -> None:
        """Render a registered view."""

        if name not in self._view_factories:
            raise KeyError(f"View is not registered: {name}")

        if self._current_view is not None:
            self._current_view.destroy()

        self._current_view = self._view_factories[name](self.root, self.context)
        self._current_view.pack(fill="both", expand=True)

    def run(self) -> None:
        """Start the GUI event loop."""

        self.root.mainloop()

