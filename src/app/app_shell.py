"""
File Purpose: Application shell coordinator for startup and routing.
Module: app.app_shell
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: typing, app.controllers, app.database, app.repositories, app.services, app.startup, app.ui.
"""

from typing import Optional

from app.controllers.auth_controller import AuthController
from app.database.initializer import initialize_database
from app.models.session import UserSession
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.startup import ApplicationContext
from app.ui.app_shell import AppShell
from app.ui.login_view import LoginView
from app.ui.window_manager import WindowManager


class ApplicationShell:
    """Coordinates startup, login, and authenticated shell routing."""

    LOGIN_VIEW = "login"
    APP_VIEW = "app"

    def __init__(self, context: ApplicationContext) -> None:
        self.context = context
        self.window_manager = WindowManager(context)
        self.user_repository = UserRepository(context.database)
        self.auth_service = AuthService(self.user_repository)
        self._session: Optional[UserSession] = None

    def prepare(self) -> None:
        """Initialize database and register application views."""

        initialize_database(self.context.database, self.context.paths)
        self.window_manager.register_view(self.LOGIN_VIEW, self._build_login_view)
        self.window_manager.register_view(self.APP_VIEW, self._build_app_view)

    def run(self) -> None:
        """Show login and start GUI loop."""

        self.prepare()
        self.window_manager.show_view(self.LOGIN_VIEW)
        self.context.logger.info("Application shell started")
        self.window_manager.run()

    def _build_login_view(self, master, _context):
        controller = AuthController(
            self.auth_service,
            on_login_success=self._handle_login_success,
        )
        return LoginView(master, controller)

    def _build_app_view(self, master, _context):
        if self._session is None:
            raise RuntimeError("Cannot build app shell without an authenticated session")
        return AppShell(master, self._session, self.context.database, self.context.paths)

    def _handle_login_success(self, session: UserSession) -> None:
        self._session = session
        self.context.logger.info("User logged in: %s", session.user.username)
        self.window_manager.show_view(self.APP_VIEW)
