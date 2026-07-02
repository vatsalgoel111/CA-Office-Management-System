"""
File Purpose: Reports and CSV export view using reusable UI components.
Module: app.ui.report_view
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: customtkinter, app.controllers.report_controller, app.models, app.ui.
"""

import customtkinter as ctk

from app.controllers.report_controller import ReportController
from app.models.report import ReportTable
from app.ui.components import DataTable, PrimaryButton, SecondaryButton
from app.ui.theme import theme_manager


class ReportView(ctk.CTkFrame):
    """Report preview and CSV export foundation view."""

    def __init__(self, master, controller: ReportController, **kwargs) -> None:
        super().__init__(master, fg_color=theme_manager.color("bg"), **kwargs)
        self._controller = controller
        self._reports = controller.available_reports()
        self._current_key = next(iter(self._reports))
        self._table = None
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self._build()
        self._load_report()

    def _build(self) -> None:
        ctk.CTkLabel(
            self,
            text="Reports",
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.page, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(24, 8))

        ctk.CTkLabel(
            self,
            text="Preview operational reports and export CSV files.",
            text_color=theme_manager.color("text_muted"),
            font=theme_manager.font(theme_manager.tokens.fonts.body),
        ).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 16))

        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=2, column=0, sticky="ew", padx=24, pady=(0, 16))
        toolbar.grid_columnconfigure(0, weight=1)

        self.report_selector = ctk.CTkOptionMenu(
            toolbar,
            values=list(self._reports.values()),
            command=self._select_report,
            fg_color=theme_manager.color("surface_alt"),
            button_color=theme_manager.color("primary"),
            button_hover_color=theme_manager.color("primary_hover"),
            text_color=theme_manager.color("text"),
            dropdown_fg_color=theme_manager.color("surface"),
            dropdown_text_color=theme_manager.color("text"),
            width=260,
        )
        self.report_selector.grid(row=0, column=0, sticky="w")

        SecondaryButton(toolbar, "Refresh", command=self._load_report).grid(
            row=0,
            column=1,
            padx=(8, 0),
        )
        PrimaryButton(toolbar, "Export CSV", command=self._export_csv).grid(
            row=0,
            column=2,
            padx=(8, 0),
        )

        self.message_label = ctk.CTkLabel(
            self,
            text="",
            text_color=theme_manager.color("text_muted"),
            font=theme_manager.font(theme_manager.tokens.fonts.small),
        )
        self.message_label.grid(row=3, column=0, sticky="w", padx=24, pady=(0, 8))

        self.table_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.table_frame.grid(row=4, column=0, sticky="nsew", padx=24, pady=(0, 24))
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)

    def _select_report(self, label: str) -> None:
        for key, report_label in self._reports.items():
            if report_label == label:
                self._current_key = key
                break
        self._load_report()

    def _load_report(self) -> None:
        report, error = self._controller.build_report(self._current_key)
        if error or report is None:
            self.message_label.configure(text=error or "Unable to load report")
            return
        self._render_report(report)
        self.message_label.configure(text=f"{report.title}: {report.row_count} rows")

    def _render_report(self, report: ReportTable) -> None:
        for child in self.table_frame.winfo_children():
            child.destroy()
        self._table = DataTable(self.table_frame, report.columns)
        self._table.grid(row=0, column=0, sticky="nsew")
        self._table.set_rows(report.rows)

    def _export_csv(self) -> None:
        result, error = self._controller.export_csv(self._current_key)
        if error or result is None:
            self.message_label.configure(text=error or "Export failed")
            return
        self.message_label.configure(
            text=f"Exported {result.row_count} rows to {result.file_path}"
        )
