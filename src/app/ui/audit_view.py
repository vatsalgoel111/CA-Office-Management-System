"""
File Purpose: Audit log viewer using reusable UI components.
Module: app.ui.audit_view
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, customtkinter, app.controllers.audit_controller, app.models, app.ui.
"""

from typing import List

import customtkinter as ctk

from app.controllers.audit_controller import AuditController
from app.models.audit import AuditLogEntry
from app.ui.components import DataTable, SearchBox
from app.ui.theme import theme_manager


class AuditView(ctk.CTkFrame):
    """Read-only audit log viewer."""

    COLUMNS = ("Time", "User", "Action", "Entity", "ID", "Description")

    def __init__(self, master, controller: AuditController, **kwargs) -> None:
        super().__init__(master, fg_color=theme_manager.color("bg"), **kwargs)
        self._controller = controller
        self._entries: List[AuditLogEntry] = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self._build()
        self._refresh()

    def _build(self) -> None:
        ctk.CTkLabel(
            self,
            text="Audit Log",
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.page, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(24, 8))

        ctk.CTkLabel(
            self,
            text="Review important system and business events.",
            text_color=theme_manager.color("text_muted"),
            font=theme_manager.font(theme_manager.tokens.fonts.body),
        ).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 16))

        self.search_box = SearchBox(self, "Search audit log", self._refresh)
        self.search_box.grid(row=2, column=0, sticky="ew", padx=24, pady=(0, 16))

        self.table = DataTable(self, self.COLUMNS)
        self.table.grid(row=3, column=0, sticky="nsew", padx=24, pady=(0, 24))

    def _refresh(self, search_text: str = "") -> None:
        search = search_text if search_text else self.search_box.get()
        self._entries = self._controller.list_entries(search)
        self.table.set_rows(
            (
                entry.created_at,
                entry.username or "system",
                entry.action,
                entry.entity_type,
                entry.entity_id or "",
                entry.description,
            )
            for entry in self._entries
        )
