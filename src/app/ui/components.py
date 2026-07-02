"""
File Purpose: Reusable CustomTkinter UI component library.
Module: app.ui.components
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: datetime, typing, customtkinter, tkcalendar, app.models.lookup, app.ui.theme.
"""

from datetime import date
from typing import Callable, Iterable, List, Optional, Sequence

import customtkinter as ctk
from tkcalendar import DateEntry

from app.models.lookup import LookupChoice
from app.ui.theme import theme_manager


Command = Optional[Callable[[], None]]


class PrimaryButton(ctk.CTkButton):
    """Primary action button."""

    def __init__(self, master, text: str, command: Command = None, **kwargs) -> None:
        super().__init__(
            master,
            text=text,
            command=command,
            fg_color=theme_manager.color("primary"),
            hover_color=theme_manager.color("primary_hover"),
            text_color=("#FFFFFF", "#FFFFFF"),
            corner_radius=theme_manager.tokens.radius.md,
            font=theme_manager.font(theme_manager.tokens.fonts.body, "bold"),
            **kwargs,
        )


class SecondaryButton(ctk.CTkButton):
    """Secondary action button."""

    def __init__(self, master, text: str, command: Command = None, **kwargs) -> None:
        super().__init__(
            master,
            text=text,
            command=command,
            fg_color=theme_manager.color("surface_alt"),
            hover_color=theme_manager.color("border"),
            border_color=theme_manager.color("border"),
            border_width=1,
            text_color=theme_manager.color("text"),
            corner_radius=theme_manager.tokens.radius.md,
            font=theme_manager.font(theme_manager.tokens.fonts.body),
            **kwargs,
        )


class IconButton(ctk.CTkButton):
    """Compact icon or icon-text button."""

    def __init__(self, master, text: str, command: Command = None, **kwargs) -> None:
        super().__init__(
            master,
            text=text,
            command=command,
            width=36,
            height=32,
            fg_color="transparent",
            hover_color=theme_manager.color("surface_alt"),
            text_color=theme_manager.color("text"),
            corner_radius=theme_manager.tokens.radius.sm,
            font=theme_manager.font(theme_manager.tokens.fonts.body),
            **kwargs,
        )


class SearchBox(ctk.CTkFrame):
    """Search input with a consistent business UI layout."""

    def __init__(
        self,
        master,
        placeholder: str = "Search",
        on_search: Optional[Callable[[str], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self._on_search = on_search
        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            border_color=theme_manager.color("border"),
            fg_color=theme_manager.color("surface"),
            text_color=theme_manager.color("text"),
        )
        self.entry.pack(side="left", fill="x", expand=True)
        self.button = SecondaryButton(self, "Search", command=self.search)
        self.button.pack(side="left", padx=(theme_manager.tokens.spacing.sm, 0))
        self.entry.bind("<Return>", lambda _event: self.search())

    def get(self) -> str:
        """Return current search text."""

        return self.entry.get().strip()

    def search(self) -> None:
        """Trigger the configured search callback."""

        if self._on_search:
            self._on_search(self.get())


class SearchableDropdown(ctk.CTkFrame):
    """Searchable ID-backed dropdown that displays business labels."""

    def __init__(
        self,
        master,
        label: str,
        required: bool = False,
        placeholder: str = "Search",
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self._choices: List[LookupChoice] = []
        self._filtered: List[LookupChoice] = []
        self._selected: Optional[LookupChoice] = None

        display_label = f"{label} *" if required else label
        ctk.CTkLabel(
            self,
            text=display_label,
            anchor="w",
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.body, "bold"),
        ).pack(fill="x")
        self.search_input = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            border_color=theme_manager.color("border"),
            fg_color=theme_manager.color("surface"),
            text_color=theme_manager.color("text"),
        )
        self.search_input.pack(fill="x", pady=(theme_manager.tokens.spacing.xs, 4))
        self.option = ctk.CTkOptionMenu(
            self,
            values=["No options"],
            command=self._select_display,
            fg_color=theme_manager.color("surface_alt"),
            button_color=theme_manager.color("primary"),
            button_hover_color=theme_manager.color("primary_hover"),
            text_color=theme_manager.color("text"),
            dropdown_fg_color=theme_manager.color("surface"),
            dropdown_text_color=theme_manager.color("text"),
        )
        self.option.pack(fill="x")
        self.error_label = ctk.CTkLabel(
            self,
            text="",
            anchor="w",
            text_color=theme_manager.color("error"),
            font=theme_manager.font(theme_manager.tokens.fonts.small),
        )
        self.error_label.pack(fill="x")
        self.search_input.bind("<KeyRelease>", lambda _event: self._filter())

    def set_choices(self, choices: Sequence[LookupChoice]) -> None:
        """Replace dropdown choices."""

        current_id = self.get_selected_id()
        self._choices = list(choices)
        self._filtered = list(self._choices)
        self._selected = None
        if current_id is not None:
            self._selected = next(
                (choice for choice in self._choices if choice.id == current_id),
                None,
            )
        self._sync_values()

    def get_selected_id(self) -> Optional[int]:
        """Return selected choice ID."""

        return self._selected.id if self._selected else None

    def clear(self) -> None:
        """Clear selection and search text."""

        self._selected = None
        self.search_input.delete(0, "end")
        self._filtered = list(self._choices)
        self._sync_values()
        self.clear_error()

    def set_error(self, message: str) -> None:
        """Show validation error text."""

        self.error_label.configure(text=message)

    def clear_error(self) -> None:
        """Clear validation error text."""

        self.error_label.configure(text="")

    def _filter(self) -> None:
        search = self.search_input.get().strip().lower()
        self._filtered = [
            choice for choice in self._choices if search in choice.display.lower()
        ]
        self._selected = None
        self._sync_values()

    def _sync_values(self) -> None:
        values = [choice.display for choice in self._filtered] or ["No options"]
        self.option.configure(values=values)
        if self._selected is not None:
            self.option.set(self._selected.display)
            return
        self.option.set(values[0])
        if self._filtered:
            self._selected = self._filtered[0]

    def _select_display(self, display: str) -> None:
        self._selected = next(
            (choice for choice in self._filtered if choice.display == display),
            None,
        )


class DatePickerField(ctk.CTkFrame):
    """Calendar date picker using tkcalendar."""

    def __init__(self, master, label: str, required: bool = False, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        display_label = f"{label} *" if required else label
        ctk.CTkLabel(
            self,
            text=display_label,
            anchor="w",
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.body, "bold"),
        ).pack(fill="x")
        self.input = DateEntry(
            self,
            date_pattern="yyyy-mm-dd",
            width=14,
            background=theme_manager.color("primary"),
            foreground="white",
            borderwidth=1,
        )
        self.input.pack(fill="x", pady=(theme_manager.tokens.spacing.xs, 0))
        self.error_label = ctk.CTkLabel(
            self,
            text="",
            anchor="w",
            text_color=theme_manager.color("error"),
            font=theme_manager.font(theme_manager.tokens.fonts.small),
        )
        self.error_label.pack(fill="x")

    def get(self) -> str:
        """Return selected date as ISO text."""

        return self.input.get_date().isoformat()

    def clear(self) -> None:
        """Reset date to today."""

        self.input.set_date(date.today())
        self.clear_error()

    def set_error(self, message: str) -> None:
        """Show validation error text."""

        self.error_label.configure(text=message)

    def clear_error(self) -> None:
        """Clear validation error text."""

        self.error_label.configure(text="")


class StatusBadge(ctk.CTkLabel):
    """Readable status label using text and color."""

    STATUS_COLOR_MAP = {
        "completed": "success",
        "paid": "success",
        "pending": "warning",
        "partial": "warning",
        "overdue": "error",
        "unpaid": "error",
        "failed": "error",
        "in progress": "info",
        "waiting for client": "info",
        "on hold": "neutral",
        "cancelled": "neutral",
    }

    def __init__(self, master, status: str, **kwargs) -> None:
        token = self.STATUS_COLOR_MAP.get(status.lower(), "neutral")
        super().__init__(
            master,
            text=status,
            fg_color=theme_manager.color(token),
            text_color=("#FFFFFF", "#101418"),
            corner_radius=theme_manager.tokens.radius.sm,
            padx=theme_manager.tokens.spacing.sm,
            pady=theme_manager.tokens.spacing.xs,
            font=theme_manager.font(theme_manager.tokens.fonts.small, "bold"),
            **kwargs,
        )


class InfoCard(ctk.CTkFrame):
    """Compact dashboard or summary card."""

    def __init__(self, master, title: str, value: str, subtitle: str = "", **kwargs) -> None:
        super().__init__(
            master,
            fg_color=theme_manager.color("surface"),
            border_color=theme_manager.color("border"),
            border_width=1,
            corner_radius=theme_manager.tokens.radius.lg,
            **kwargs,
        )
        padding = theme_manager.tokens.spacing.lg
        self.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            self,
            text=title,
            text_color=theme_manager.color("text_muted"),
            font=theme_manager.font(theme_manager.tokens.fonts.small),
        ).grid(row=0, column=0, sticky="w", padx=padding, pady=(padding, 0))
        ctk.CTkLabel(
            self,
            text=value,
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.metric, "bold"),
        ).grid(row=1, column=0, sticky="w", padx=padding, pady=(4, 0))
        if subtitle:
            ctk.CTkLabel(
                self,
                text=subtitle,
                text_color=theme_manager.color("text_muted"),
                font=theme_manager.font(theme_manager.tokens.fonts.small),
            ).grid(row=2, column=0, sticky="w", padx=padding, pady=(4, padding))


class FormField(ctk.CTkFrame):
    """Label, input, and validation message wrapper."""

    def __init__(
        self,
        master,
        label: str,
        required: bool = False,
        placeholder: str = "",
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        display_label = f"{label} *" if required else label
        ctk.CTkLabel(
            self,
            text=display_label,
            anchor="w",
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.body, "bold"),
        ).pack(fill="x")
        self.input = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            border_color=theme_manager.color("border"),
            fg_color=theme_manager.color("surface"),
            text_color=theme_manager.color("text"),
        )
        self.input.pack(fill="x", pady=(theme_manager.tokens.spacing.xs, 0))
        self.error_label = ctk.CTkLabel(
            self,
            text="",
            anchor="w",
            text_color=theme_manager.color("error"),
            font=theme_manager.font(theme_manager.tokens.fonts.small),
        )
        self.error_label.pack(fill="x")

    def get(self) -> str:
        """Return current field value."""

        return self.input.get().strip()

    def set_error(self, message: str) -> None:
        """Show validation error text."""

        self.error_label.configure(text=message)

    def clear_error(self) -> None:
        """Clear validation error text."""

        self.error_label.configure(text="")


class DataTable(ctk.CTkScrollableFrame):
    """Simple reusable table for business data."""

    def __init__(
        self,
        master,
        columns: Sequence[str],
        on_sort: Optional[Callable[[str], None]] = None,
        empty_message: str = "No records found.",
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color=theme_manager.color("surface"), **kwargs)
        self.columns = list(columns)
        self.on_sort = on_sort
        self.empty_message = empty_message
        self.rows: List[Sequence[str]] = []
        self._render_header()

    def _render_header(self) -> None:
        for index, column in enumerate(self.columns):
            header = ctk.CTkButton(
                self,
                text=column,
                command=lambda col=column: self._sort(col),
                fg_color=theme_manager.color("surface_alt"),
                hover_color=theme_manager.color("border"),
                text_color=theme_manager.color("text"),
                corner_radius=0,
                font=theme_manager.font(theme_manager.tokens.fonts.body, "bold"),
            )
            header.grid(row=0, column=index, sticky="ew", padx=1, pady=1)
            self.grid_columnconfigure(index, weight=1)

    def set_rows(self, rows: Iterable[Sequence[str]]) -> None:
        """Replace table rows."""

        for child in self.winfo_children():
            info = child.grid_info()
            if int(info.get("row", 0)) > 0:
                child.destroy()

        self.rows = list(rows)
        if not self.rows:
            ctk.CTkLabel(
                self,
                text=self.empty_message,
                anchor="center",
                fg_color=theme_manager.color("surface"),
                text_color=theme_manager.color("text_muted"),
                font=theme_manager.font(theme_manager.tokens.fonts.body),
                padx=theme_manager.tokens.spacing.lg,
                pady=theme_manager.tokens.spacing.lg,
            ).grid(
                row=1,
                column=0,
                columnspan=max(len(self.columns), 1),
                sticky="ew",
                padx=1,
                pady=1,
            )
            return
        for row_index, row in enumerate(self.rows, start=1):
            row_color = "surface" if row_index % 2 else "surface_alt"
            for column_index, value in enumerate(row):
                ctk.CTkLabel(
                    self,
                    text=str(value),
                    anchor="w",
                    fg_color=theme_manager.color(row_color),
                    text_color=theme_manager.color("text"),
                    font=theme_manager.font(theme_manager.tokens.fonts.body),
                    padx=theme_manager.tokens.spacing.sm,
                    pady=theme_manager.tokens.spacing.sm,
                ).grid(row=row_index, column=column_index, sticky="ew", padx=1, pady=1)

    def _sort(self, column: str) -> None:
        if self.on_sort:
            self.on_sort(column)


class Sidebar(ctk.CTkFrame):
    """Left navigation sidebar."""

    def __init__(self, master, title: str = "CA Office CMS", **kwargs) -> None:
        super().__init__(
            master,
            width=220,
            fg_color=theme_manager.color("surface_alt"),
            corner_radius=0,
            **kwargs,
        )
        self.pack_propagate(False)
        ctk.CTkLabel(
            self,
            text=title,
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.section, "bold"),
        ).pack(fill="x", padx=theme_manager.tokens.spacing.lg, pady=theme_manager.tokens.spacing.lg)
        self.items_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.items_frame.pack(fill="both", expand=True)
        self._buttons = {}

    def add_item(
        self,
        key: str,
        label: str,
        command: Command = None,
        active: bool = False,
    ) -> None:
        """Add a navigation item."""

        button = ctk.CTkButton(
            self.items_frame,
            text=label,
            command=command,
            fg_color=theme_manager.color("primary") if active else "transparent",
            hover_color=theme_manager.color("primary_hover")
            if active
            else theme_manager.color("surface"),
            text_color=("#FFFFFF", "#FFFFFF") if active else theme_manager.color("text"),
            corner_radius=theme_manager.tokens.radius.md,
            font=theme_manager.font(theme_manager.tokens.fonts.body, "bold" if active else "normal"),
        )
        button.configure(anchor="w", width=180)
        button.pack(fill="x", padx=theme_manager.tokens.spacing.md, pady=theme_manager.tokens.spacing.xs)
        self._buttons[key] = button

    def set_active(self, active_key: str) -> None:
        """Update active sidebar button."""

        for key, button in self._buttons.items():
            is_active = key == active_key
            button.configure(
                fg_color=theme_manager.color("primary") if is_active else "transparent",
                hover_color=theme_manager.color("primary_hover")
                if is_active
                else theme_manager.color("surface"),
                text_color=("#FFFFFF", "#FFFFFF")
                if is_active
                else theme_manager.color("text"),
                font=theme_manager.font(
                    theme_manager.tokens.fonts.body,
                    "bold" if is_active else "normal",
                ),
            )


class TopBar(ctk.CTkFrame):
    """Top navigation/header bar."""

    def __init__(self, master, title: str, **kwargs) -> None:
        super().__init__(
            master,
            height=56,
            fg_color=theme_manager.color("surface"),
            corner_radius=0,
            **kwargs,
        )
        self.pack_propagate(False)
        ctk.CTkLabel(
            self,
            text=title,
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.section, "bold"),
        ).pack(side="left", padx=theme_manager.tokens.spacing.lg)


class ConfirmationDialog(ctk.CTkToplevel):
    """Reusable confirmation dialog."""

    def __init__(
        self,
        master,
        title: str,
        message: str,
        on_confirm: Command = None,
    ) -> None:
        super().__init__(master)
        self.title(title)
        self.geometry("420x180")
        self.resizable(False, False)
        self._on_confirm = on_confirm
        self.configure(fg_color=theme_manager.color("bg"))
        ctk.CTkLabel(
            self,
            text=message,
            wraplength=360,
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.body),
        ).pack(fill="both", expand=True, padx=theme_manager.tokens.spacing.xl, pady=theme_manager.tokens.spacing.lg)
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=theme_manager.tokens.spacing.xl, pady=(0, theme_manager.tokens.spacing.lg))
        SecondaryButton(actions, "Cancel", command=self.destroy).pack(side="right")
        PrimaryButton(actions, "Confirm", command=self._confirm).pack(
            side="right",
            padx=(0, theme_manager.tokens.spacing.sm),
        )

    def _confirm(self) -> None:
        if self._on_confirm:
            self._on_confirm()
        self.destroy()


class LoadingOverlay(ctk.CTkFrame):
    """Simple loading overlay for long-running actions."""

    def __init__(self, master, message: str = "Loading...", **kwargs) -> None:
        super().__init__(master, fg_color=theme_manager.color("bg"), **kwargs)
        ctk.CTkLabel(
            self,
            text=message,
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.section, "bold"),
        ).place(relx=0.5, rely=0.5, anchor="center")


class NotificationToast(ctk.CTkFrame):
    """Non-blocking notification banner."""

    def __init__(self, master, message: str, status: str = "info", **kwargs) -> None:
        super().__init__(
            master,
            fg_color=theme_manager.color(status if status in theme_manager.tokens.colors else "info"),
            corner_radius=theme_manager.tokens.radius.lg,
            **kwargs,
        )
        ctk.CTkLabel(
            self,
            text=message,
            text_color=("#FFFFFF", "#101418"),
            font=theme_manager.font(theme_manager.tokens.fonts.body, "bold"),
        ).pack(padx=theme_manager.tokens.spacing.lg, pady=theme_manager.tokens.spacing.md)
