"""
File Purpose: Login screen built from reusable UI components.
Module: app.ui.login_view
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: customtkinter, app.controllers.auth_controller, app.ui.
"""

import customtkinter as ctk

from app.controllers.auth_controller import AuthController
from app.ui.components import FormField, PrimaryButton
from app.ui.theme import theme_manager


class LoginView(ctk.CTkFrame):
    """Login view for application users."""

    def __init__(self, master, controller: AuthController, **kwargs) -> None:
        super().__init__(master, fg_color=theme_manager.color("bg"), **kwargs)
        self._controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        panel = ctk.CTkFrame(
            self,
            width=420,
            fg_color=theme_manager.color("surface"),
            border_color=theme_manager.color("border"),
            border_width=1,
            corner_radius=theme_manager.tokens.radius.lg,
        )
        panel.grid(row=0, column=0, sticky="")
        panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            panel,
            text="CA Office Management",
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.page, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=32, pady=(32, 8))

        ctk.CTkLabel(
            panel,
            text="Sign in to continue",
            text_color=theme_manager.color("text_muted"),
            font=theme_manager.font(theme_manager.tokens.fonts.body),
        ).grid(row=1, column=0, sticky="w", padx=32, pady=(0, 24))

        self.username = FormField(panel, "Username", required=True)
        self.username.grid(row=2, column=0, sticky="ew", padx=32, pady=(0, 12))

        self.password = FormField(panel, "Password", required=True)
        self.password.input.configure(show="*")
        self.password.grid(row=3, column=0, sticky="ew", padx=32, pady=(0, 12))

        self.error_label = ctk.CTkLabel(
            panel,
            text="",
            text_color=theme_manager.color("error"),
            font=theme_manager.font(theme_manager.tokens.fonts.small),
        )
        self.error_label.grid(row=4, column=0, sticky="w", padx=32, pady=(0, 12))

        self.login_button = PrimaryButton(panel, "Login", command=self._login)
        self.login_button.grid(row=5, column=0, sticky="ew", padx=32, pady=(0, 32))
        self.password.input.bind("<Return>", lambda _event: self._login())

    def _login(self) -> None:
        self.username.clear_error()
        self.password.clear_error()
        self.error_label.configure(text="")

        username = self.username.get()
        password = self.password.get()
        if not username:
            self.username.set_error("Username is required")
            return
        if not password:
            self.password.set_error("Password is required")
            return

        error = self._controller.login(username, password)
        if error:
            self.error_label.configure(text=error)

