"""User database module for terminal chatbot.

This module uses JSON for persistence and PBKDF2-HMAC-SHA256 for password hashing.
Only Python built-in modules are used.
"""

from __future__ import annotations

import json
import os
import hashlib
import secrets
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class UserDatabase:
    """Simple JSON-backed user database with secure password handling."""

    def __init__(self, db_file: str = "users.json") -> None:
        self.db_file = db_file
        self.data: Dict[str, Dict[str, Any]] = {"users": {}}
        self._load_database()

    def _load_database(self) -> None:
        """Load database from disk or initialize an empty schema."""
        if not os.path.exists(self.db_file):
            self._save_database()
            return

        try:
            with open(self.db_file, "r", encoding="utf-8") as file:
                content = json.load(file)
            if isinstance(content, dict) and "users" in content and isinstance(content["users"], dict):
                self.data = content
            else:
                self.data = {"users": {}}
                self._save_database()
        except (json.JSONDecodeError, OSError):
            self.data = {"users": {}}
            self._save_database()

    def _save_database(self) -> None:
        """Persist database to disk safely."""
        os.makedirs(os.path.dirname(os.path.abspath(self.db_file)), exist_ok=True)
        with open(self.db_file, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=2, ensure_ascii=False)

    def _hash_password(self, password: str, salt: Optional[str] = None) -> str:
        """Hash a password using PBKDF2-HMAC-SHA256 with 100000 iterations.

        Returns a storage string with format: ``salt$hash``.
        """
        password = password or ""
        salt = salt or secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100000,
        ).hex()
        return f"{salt}${hashed}"

    def _verify_password(self, password: str, stored_hash: str) -> bool:
        """Validate a plaintext password against a stored hash."""
        try:
            salt, hashed = stored_hash.split("$", 1)
        except ValueError:
            return False

        check = hashlib.pbkdf2_hmac(
            "sha256",
            (password or "").encode("utf-8"),
            salt.encode("utf-8"),
            100000,
        ).hex()
        return secrets.compare_digest(hashed, check)

    def user_exists(self, username: str) -> bool:
        """Return True if the username already exists."""
        return username in self.data["users"]

    def create_user(self, username: str, password: str, display_name: Optional[str] = None) -> bool:
        """Create a new user.

        Returns True on success and False if user exists or input invalid.
        """
        username = (username or "").strip()
        if not username or not password or self.user_exists(username):
            return False

        self.data["users"][username] = {
            "username": username,
            "password_hash": self._hash_password(password),
            "display_name": display_name.strip() if display_name else username,
            "theme": "default",
            "chat_history": [],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._save_database()
        return True

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user credentials."""
        user = self.data["users"].get((username or "").strip())
        if not user:
            return False
        return self._verify_password(password, user.get("password_hash", ""))

    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get a user dictionary without exposing mutable internal structure."""
        user = self.data["users"].get((username or "").strip())
        if user is None:
            return None
        return dict(user)

    def update_user(self, username: str, updates: Dict[str, Any]) -> bool:
        """Update mutable user settings (display_name/theme)."""
        username = (username or "").strip()
        if username not in self.data["users"] or not isinstance(updates, dict):
            return False

        allowed_keys = {"display_name", "theme"}
        for key, value in updates.items():
            if key in allowed_keys:
                self.data["users"][username][key] = value

        self._save_database()
        return True

    def add_to_chat_history(self, username: str, user_message: str, bot_response: str) -> bool:
        """Append a chat exchange to user history."""
        username = (username or "").strip()
        if username not in self.data["users"]:
            return False

        self.data["users"][username].setdefault("chat_history", []).append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "user_message": user_message,
                "bot_response": bot_response,
            }
        )
        self._save_database()
        return True

    def get_chat_history(self, username: str) -> List[Dict[str, Any]]:
        """Return chat history for a user."""
        username = (username or "").strip()
        user = self.data["users"].get(username)
        if not user:
            return []
        history = user.get("chat_history", [])
        return list(history) if isinstance(history, list) else []

    def clear_chat_history(self, username: str) -> bool:
        """Clear chat history for a user."""
        username = (username or "").strip()
        if username not in self.data["users"]:
            return False

        self.data["users"][username]["chat_history"] = []
        self._save_database()
        return True

    def delete_user(self, username: str) -> bool:
        """Delete a user account permanently."""
        username = (username or "").strip()
        if username not in self.data["users"]:
            return False

        del self.data["users"][username]
        self._save_database()
        return True

    def change_password(self, username: str, current_password: str, new_password: str) -> bool:
        """Change password after validating current credentials."""
        username = (username or "").strip()
        if username not in self.data["users"] or not new_password:
            return False
        if not self.authenticate(username, current_password):
            return False

        self.data["users"][username]["password_hash"] = self._hash_password(new_password)
        self._save_database()
        return True
