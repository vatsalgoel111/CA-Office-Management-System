"""
File Purpose: Settings view using reusable UI components.
Module: app.ui.setting_view
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, customtkinter, app.controllers.setting_controller, app.models, app.ui.
"""

from typing import List

import customtkinter as ctk

from app.controllers.setting_controller import SettingController
from app.models.setting import Setting, SettingInput
from app.ui.components import DataTable, FormField, PrimaryButton, SecondaryButton
from app.ui.theme import theme_manager


class SettingView(ctk.CTkFrame):
    """Application settings list and update foundation view."""

    COLUMNS = ("Key", "Value", "Updated")

    def __init__(self, master, controller: SettingController, **kwargs) -> None:
        super().__init__(master, fg_color=theme_manager.color("bg"), **kwargs)
        self._controller = controller
        self._settings: List[Setting] = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self._build()
        self._refresh()

    def _build(self) -> None:
        ctk.CTkLabel(
            self,
            text="Settings",
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.page, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(24, 8))
        ctk.CTkLabel(
            self,
            text="Manage application configuration values.",
            text_color=theme_manager.color("text_muted"),
            font=theme_manager.font(theme_manager.tokens.fonts.body),
        ).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 16))

        form = ctk.CTkFrame(
            self,
            fg_color=theme_manager.color("surface"),
            border_color=theme_manager.color("border"),
            border_width=1,
            corner_radius=theme_manager.tokens.radius.lg,
        )
        form.grid(row=2, column=0, sticky="ew", padx=24, pady=(0, 16))
        form.grid_columnconfigure((0, 1), weight=1)

        self.key = FormField(form, "Setting Key", required=True)
        self.key.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        self.value = FormField(form, "Value", required=True)
        self.value.grid(row=0, column=1, sticky="ew", padx=12, pady=12)

        self.message_label = ctk.CTkLabel(
            form,
            text="",
            text_color=theme_manager.color("error"),
            font=theme_manager.font(theme_manager.tokens.fonts.small),
        )
        self.message_label.grid(row=1, column=0, sticky="w", padx=12)

        actions = ctk.CTkFrame(form, fg_color="transparent")
        actions.grid(row=1, column=1, sticky="e", padx=12, pady=(0, 12))
        SecondaryButton(actions, "Refresh", command=self._refresh).pack(side="right")
        PrimaryButton(actions, "Save", command=self._save).pack(side="right", padx=(0, 8))

        self.table = DataTable(self, self.COLUMNS)
        self.table.grid(row=4, column=0, sticky="nsew", padx=24, pady=(0, 24))

    def _refresh(self) -> None:
        self._settings = self._controller.list_settings()
        self.table.set_rows((item.key, item.value, item.updated_at) for item in self._settings)

    def _save(self) -> None:
        self.message_label.configure(text="")
        error = self._controller.update(SettingInput(self.key.get(), self.value.get()))
        if error:
            self.message_label.configure(text=error)
            return
        self._refresh()
