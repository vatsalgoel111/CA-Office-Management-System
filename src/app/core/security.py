"""
File Purpose: Password hashing and verification helpers.
Module: app.core.security
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: base64, hashlib, hmac, os.
"""

import base64
import hashlib
import hmac
import os


ALGORITHM = "pbkdf2_sha256"
DEFAULT_ITERATIONS = 260_000
SALT_BYTES = 16


def hash_password(password: str, iterations: int = DEFAULT_ITERATIONS) -> str:
    """Hash a password using PBKDF2-HMAC-SHA256."""

    if not password:
        raise ValueError("Password must not be empty")

    salt = os.urandom(SALT_BYTES)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    )
    encoded_salt = base64.b64encode(salt).decode("ascii")
    encoded_hash = base64.b64encode(password_hash).decode("ascii")
    return f"{ALGORITHM}${iterations}${encoded_salt}${encoded_hash}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify a password against a stored PBKDF2 hash string."""

    try:
        algorithm, iterations_text, encoded_salt, encoded_hash = stored_hash.split("$")
        if algorithm != ALGORITHM:
            return False
        iterations = int(iterations_text)
        salt = base64.b64decode(encoded_salt.encode("ascii"))
        expected_hash = base64.b64decode(encoded_hash.encode("ascii"))
    except (ValueError, TypeError):
        return False

    actual_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    )
    return hmac.compare_digest(actual_hash, expected_hash)

