"""
File Purpose: Application entry point for CA Office Management System.
Module: app.main
Author: CA Office CMS Development Team
Created Date: 2026-07-01
Last Modified: 2026-07-01
Dependencies: sys, app.startup, app.core.exceptions.
"""

import sys

from app.core.exceptions import CAOfficeCMSError
from app.startup import initialize_application


def main() -> int:
    """Start the application core foundation."""

    try:
        context = initialize_application()
        context.logger.info("Application startup sequence completed")
        return 0
    except CAOfficeCMSError as exc:
        print(f"Application startup failed: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

