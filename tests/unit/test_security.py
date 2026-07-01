"""
File Purpose: Unit tests for password hashing helpers.
Module: tests.unit.test_security
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: pathlib, sys, unittest.
"""

from pathlib import Path
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from app.core.security import hash_password, verify_password  # noqa: E402


class SecurityTest(unittest.TestCase):
    """Tests for password hashing and verification."""

    def test_hash_password_does_not_store_plaintext(self) -> None:
        password_hash = hash_password("StrongPassword123")

        self.assertNotIn("StrongPassword123", password_hash)
        self.assertTrue(password_hash.startswith("pbkdf2_sha256$"))

    def test_verify_password_accepts_correct_password(self) -> None:
        password_hash = hash_password("StrongPassword123")

        self.assertTrue(verify_password("StrongPassword123", password_hash))

    def test_verify_password_rejects_wrong_password(self) -> None:
        password_hash = hash_password("StrongPassword123")

        self.assertFalse(verify_password("WrongPassword", password_hash))


if __name__ == "__main__":
    unittest.main()

