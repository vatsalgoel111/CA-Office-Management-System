"""
File Purpose: Developer script for initializing the local database.
Module: scripts.init_database
Author: CA Office CMS Development Team
Created Date: 2026-07-01
Last Modified: 2026-07-01
Dependencies: pathlib, sys, app.startup, app.database.initializer.
"""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from app.database.initializer import (  # noqa: E402
    check_database_integrity,
    initialize_database,
)
from app.startup import initialize_application  # noqa: E402


def main() -> int:
    """Initialize the configured database."""

    context = initialize_application()
    initialize_database(context.database, context.paths)

    if not check_database_integrity(context.database):
        context.logger.error("Database integrity check failed")
        return 1

    context.logger.info("Database initialized successfully")
    print(f"Database initialized: {context.paths.database_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

