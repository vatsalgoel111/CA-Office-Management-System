"""
File Purpose: Notification queue view using reusable UI components.
Module: app.ui.notification_view
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, customtkinter, app.controllers, app.models, app.ui.
"""

from typing import List

import customtkinter as ctk

from app.controllers.lookup_controller import LookupController
from app.controllers.notification_controller import NotificationController
from app.models.notification import NotificationInput, NotificationRecord
from app.ui.components import (
    DataTable,
    FormField,
    PrimaryButton,
    SearchableDropdown,
    SecondaryButton,
)
from app.ui.theme import theme_manager


class NotificationView(ctk.CTkFrame):
    """Notification queue and manual WhatsApp preparation view."""

    COLUMNS = ("Created", "Recipient", "Type", "Provider", "Status", "Message")

    def __init__(
        self,
        master,
        controller: NotificationController,
        lookup_controller: LookupController,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color=theme_manager.color("bg"), **kwargs)
        self._controller = controller
        self._lookup_controller = lookup_controller
        self._notifications: List[NotificationRecord] = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self._build()
        self._refresh()

    def _build(self) -> None:
        ctk.CTkLabel(
            self,
            text="Notifications",
            text_color=theme_manager.color("text"),
            font=theme_manager.font(theme_manager.tokens.fonts.page, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(24, 8))
        ctk.CTkLabel(
            self,
            text="Queue manual and WhatsApp notifications for later delivery.",
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
        for column in range(5):
            form.grid_columnconfigure(column, weight=1)

        self.recipient_user = SearchableDropdown(form, "Recipient", required=True)
        self.recipient_user.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        self.notification_type = FormField(form, "Type", placeholder="manual")
        self.notification_type.grid(row=0, column=1, sticky="ew", padx=12, pady=12)
        self.provider = FormField(form, "Provider", placeholder="whatsapp")
        self.provider.grid(row=0, column=2, sticky="ew", padx=12, pady=12)
        self.related_work_item = SearchableDropdown(form, "Related Work")
        self.related_work_item.grid(row=0, column=3, sticky="ew", padx=12, pady=12)
        self.message = FormField(form, "Message", required=True)
        self.message.grid(row=0, column=4, sticky="ew", padx=12, pady=12)

        self.message_label = ctk.CTkLabel(
            form,
            text="",
            text_color=theme_manager.color("error"),
            font=theme_manager.font(theme_manager.tokens.fonts.small),
        )
        self.message_label.grid(row=1, column=0, columnspan=3, sticky="w", padx=12)

        actions = ctk.CTkFrame(form, fg_color="transparent")
        actions.grid(row=1, column=3, columnspan=2, sticky="e", padx=12, pady=(0, 12))
        SecondaryButton(actions, "Refresh", command=self._refresh).pack(side="right")
        PrimaryButton(actions, "Queue", command=self._queue_notification).pack(
            side="right",
            padx=(0, 8),
        )

        self.table = DataTable(self, self.COLUMNS, empty_message="No notifications queued.")
        self.table.grid(row=4, column=0, sticky="nsew", padx=24, pady=(0, 24))

    def _refresh(self) -> None:
        self.recipient_user.set_choices(self._lookup_controller.active_users())
        self.related_work_item.set_choices(self._lookup_controller.work_items())
        self._notifications = self._controller.list_notifications()
        self.table.set_rows(
            (
                item.created_at,
                item.recipient_name,
                item.notification_type,
                item.provider,
                item.status,
                item.message,
            )
            for item in self._notifications
        )

    def _queue_notification(self) -> None:
        self.message_label.configure(text="")
        recipient_id = self.recipient_user.get_selected_id()
        work_item_id = self.related_work_item.get_selected_id()
        if recipient_id is None:
            self.message_label.configure(text="Select a recipient before queueing.")
            return

        error = self._controller.queue(
            NotificationInput(
                recipient_user_id=recipient_id,
                related_work_item_id=work_item_id,
                notification_type=self.notification_type.get() or "manual",
                provider=self.provider.get() or "whatsapp",
                message=self.message.get(),
            )
        )
        if error:
            self.message_label.configure(text=error)
            return
        self._refresh()
