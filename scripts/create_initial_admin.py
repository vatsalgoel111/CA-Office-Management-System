"""
File Purpose: Developer script for creating the first administrator account.
Module: scripts.create_initial_admin
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: getpass, pathlib, sys, app.database.initializer, app.repositories, app.services.
"""

from getpass import getpass
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from app.database.initializer import initialize_database  # noqa: E402
from app.repositories.user_repository import UserRepository  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402
from app.startup import initialize_application  # noqa: E402


def main() -> int:
    """Create the first administrator account."""

    context = initialize_application()
    initialize_database(context.database, context.paths)
    user_repository = UserRepository(context.database)
    auth_service = AuthService(user_repository)

    if user_repository.count_users() > 0:
        print("Initial administrator already exists.")
        return 1

    full_name = input("Full name: ").strip()
    username = input("Username: ").strip()
    password = getpass("Password: ")
    confirm_password = getpass("Confirm password: ")

    if password != confirm_password:
        print("Passwords do not match.")
        return 1

    auth_service.create_initial_admin(
        full_name=full_name,
        username=username,
        password=password,
    )
    print("Initial administrator created successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

