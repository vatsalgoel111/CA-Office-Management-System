"""
File Purpose: Backup management view using reusable UI components.
Module: app.ui.backup_view
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, customtkinter, app.controllers.backup_controller, app.models, app.ui.
"""

from typing import List

import customtkinter as ctk

from app.controllers.backup_controller import BackupController
from app.models.backup import BackupFile
from app.ui.components import DataTable, PrimaryButton, SecondaryButton
from app.ui.theme import theme_manager


class BackupView(ctk.CTkFrame):
    """Manual backup and backup listing foundation view."""

    COLUMNS = ("Created", "File", "Size")

    def __init__(self, master, controller: BackupController, **kwargs) -> None:
        super().__init__(master, fg_color=theme_manager.color("bg"), **kwargs)
        self._controller = controller
        self._backups: List[BackupFile] = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self._build()
        self._refresh()

    def _build(self) -> None:
        ctk.CTkLabel(
            self,
            text="Backups",
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.page, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(24, 8))

        ctk.CTkLabel(
            self,
            text="Create verified local database backups.",
            text_color=theme_manager.color("text_muted"),
            font=theme_manager.font(theme_manager.tokens.fonts.body),
        ).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 16))

        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=2, column=0, sticky="ew", padx=24, pady=(0, 16))
        PrimaryButton(toolbar, "Create Backup", command=self._create_backup).pack(
            side="left"
        )
        SecondaryButton(toolbar, "Refresh", command=self._refresh).pack(
            side="left",
            padx=(8, 0),
        )

        self.message_label = ctk.CTkLabel(
            toolbar,
            text="",
            text_color=theme_manager.color("text_muted"),
            font=theme_manager.font(theme_manager.tokens.fonts.small),
        )
        self.message_label.pack(side="left", padx=(16, 0))

        self.table = DataTable(self, self.COLUMNS)
        self.table.grid(row=3, column=0, sticky="nsew", padx=24, pady=(0, 24))

    def _refresh(self) -> None:
        self._backups = self._controller.list_backups()
        self.table.set_rows(
            (
                backup.created_at,
                backup.file_path.name,
                f"{backup.size_bytes:,} bytes",
            )
            for backup in self._backups
        )

    def _create_backup(self) -> None:
        result, error = self._controller.create_backup()
        if error or result is None:
            self.message_label.configure(text=error or "Backup failed")
            return
        status = "verified" if result.integrity_ok else "created but not verified"
        self.message_label.configure(text=f"Backup {status}: {result.file_path.name}")
        self._refresh()
