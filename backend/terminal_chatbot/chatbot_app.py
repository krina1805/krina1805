"""Main terminal chatbot application."""

from __future__ import annotations

import os
import sys
from datetime import datetime

from user_database import UserDatabase
from chatbot_engine import ChatbotEngine
from ui_utils import clear_screen, print_header, print_menu, get_input_safe


class ChatbotApp:
    """Interactive terminal chatbot app with auth, settings, and privacy menus."""

    def __init__(self) -> None:
        data_path = os.path.join(os.path.dirname(__file__), "users.json")
        self.db = UserDatabase(data_path)
        self.engine = ChatbotEngine()
        self.current_user: str | None = None

    def login_signup_menu(self) -> bool:
        """Display login/signup screen. Returns False when user chooses to exit."""
        while self.current_user is None:
            clear_screen()
            print_header("Terminal Chatbot - Authentication")
            print_menu(["Login", "Sign Up", "Exit"])
            choice = get_input_safe("Choose an option (1-3):", "int")

            if choice == 1:
                username = get_input_safe("Username:")
                password = get_input_safe("Password:")
                if self.db.authenticate(username, password):
                    self.current_user = username
                    print("Login successful.")
                    input("Press Enter to continue...")
                    return True
                print("Invalid username or password.")
                input("Press Enter to try again...")

            elif choice == 2:
                username = get_input_safe("Choose username:")
                password = get_input_safe("Choose password (min 8 chars):")
                display_name = get_input_safe("Display name:")
                if len(password) < 8:
                    print("Password must be at least 8 characters.")
                    input("Press Enter to continue...")
                    continue
                if self.db.create_user(username, password, display_name):
                    print("Account created successfully. You can now login.")
                else:
                    print("Username already exists or invalid input.")
                input("Press Enter to continue...")

            elif choice == 3:
                return False
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")

        return True

    def settings_menu(self) -> None:
        """User settings menu."""
        if self.current_user is None:
            return

        while True:
            clear_screen()
            print_header("Settings")
            print_menu([
                "Change display name",
                "Change theme",
                "Change password",
                "Back",
            ])
            choice = get_input_safe("Choose an option:", "int")

            if choice == 1:
                new_name = get_input_safe("New display name:")
                self.db.update_user(self.current_user, {"display_name": new_name})
                print("Display name updated.")
                input("Press Enter to continue...")
            elif choice == 2:
                theme = get_input_safe("Theme (default/dark/light/neon):")
                self.db.update_user(self.current_user, {"theme": theme})
                print("Theme updated.")
                input("Press Enter to continue...")
            elif choice == 3:
                current = get_input_safe("Current password:")
                new = get_input_safe("New password:")
                if len(new) < 8:
                    print("New password must be at least 8 characters.")
                elif self.db.change_password(self.current_user, current, new):
                    print("Password changed successfully.")
                else:
                    print("Password change failed. Check current password.")
                input("Press Enter to continue...")
            elif choice == 4:
                return
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")

    def privacy_menu(self) -> None:
        """Privacy and data controls."""
        if self.current_user is None:
            return

        while True:
            clear_screen()
            print_header("Privacy & Data")
            print_menu([
                "View account data",
                "View chat history",
                "Clear chat history",
                "Delete account",
                "Back",
            ])
            choice = get_input_safe("Choose an option:", "int")

            if choice == 1:
                user = self.db.get_user(self.current_user)
                if user:
                    print(f"Username: {user.get('username')}")
                    print(f"Display Name: {user.get('display_name')}")
                    print(f"Theme: {user.get('theme')}")
                    print(f"Created At: {user.get('created_at')}")
                input("Press Enter to continue...")

            elif choice == 2:
                history = self.db.get_chat_history(self.current_user)
                if not history:
                    print("No history available.")
                else:
                    for row in history[-20:]:
                        print("-" * 40)
                        print(f"[{row.get('timestamp')}] You: {row.get('user_message')}")
                        print(f"Bot: {row.get('bot_response')}")
                input("Press Enter to continue...")

            elif choice == 3:
                if get_input_safe("Are you sure you want to clear history? (yes/no):", "yesno"):
                    self.db.clear_chat_history(self.current_user)
                    print("Chat history cleared.")
                input("Press Enter to continue...")

            elif choice == 4:
                confirm = get_input_safe("Type your password to delete account:")
                if self.db.authenticate(self.current_user, confirm):
                    self.db.delete_user(self.current_user)
                    self.current_user = None
                    print("Account deleted.")
                    input("Press Enter to continue...")
                    return
                print("Incorrect password.")
                input("Press Enter to continue...")

            elif choice == 5:
                return
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")

    def chat_menu(self) -> None:
        """Main chat interface for logged-in user."""
        if self.current_user is None:
            return

        while True:
            clear_screen()
            user = self.db.get_user(self.current_user) or {}
            display_name = user.get("display_name", self.current_user)
            print_header(f"Chat Session - {display_name}")
            print("Type your message below. Type /menu to return.")
            print("Type /history for recent messages.")
            user_input = input("You: ").strip()

            if not user_input:
                continue
            if user_input == "/menu":
                return
            if user_input == "/history":
                history = self.db.get_chat_history(self.current_user)[-10:]
                for row in history:
                    print(f"[{row.get('timestamp')}] You: {row.get('user_message')}")
                    print(f"Bot: {row.get('bot_response')}")
                input("Press Enter to continue...")
                continue

            response = self.engine.get_response(user_input)
            print(f"Bot: {response}")
            self.db.add_to_chat_history(self.current_user, user_input, response)
            input("Press Enter to continue...")

    def main_loop(self) -> None:
        """Run application loop."""
        while True:
            if self.current_user is None and not self.login_signup_menu():
                clear_screen()
                print("Goodbye!")
                return

            clear_screen()
            print_header("Terminal Chatbot")
            print_menu([
                "Start chat",
                "Settings",
                "Privacy",
                "Logout",
                "Exit",
            ])
            choice = get_input_safe("Choose an option:", "int")

            if choice == 1:
                self.chat_menu()
            elif choice == 2:
                self.settings_menu()
            elif choice == 3:
                self.privacy_menu()
            elif choice == 4:
                self.current_user = None
            elif choice == 5:
                clear_screen()
                print(f"Session ended at {datetime.now().isoformat(timespec='seconds')}")
                print("Goodbye!")
                return
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        ChatbotApp().main_loop()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting...")
        sys.exit(0)
