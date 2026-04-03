"""Terminal UI utilities for chatbot app using ANSI escape codes only."""

from __future__ import annotations

import os
from typing import List


RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"


def clear_screen() -> None:
    """Clear terminal screen on Windows/Linux/macOS."""
    os.system("cls" if os.name == "nt" else "clear")


def print_header(title: str) -> None:
    """Print a stylized app header."""
    bar = "=" * 64
    print(f"{MAGENTA}{BOLD}{bar}{RESET}")
    print(f"{CYAN}{BOLD}{title.center(64)}{RESET}")
    print(f"{MAGENTA}{BOLD}{bar}{RESET}")


def print_menu(options: List[str]) -> None:
    """Print numbered menu options."""
    for index, option in enumerate(options, start=1):
        print(f"{YELLOW}{index:>2}.{RESET} {option}")


def get_input_safe(prompt: str, input_type: str = "str"):
    """Get validated user input.

    Supported input types: 'str', 'int', 'yesno'.
    """
    while True:
        value = input(f"{GREEN}{prompt}{RESET} ").strip()

        if input_type == "str":
            if value:
                return value
            print(f"{RED}Input cannot be empty.{RESET}")
            continue

        if input_type == "int":
            try:
                return int(value)
            except ValueError:
                print(f"{RED}Please enter a valid number.{RESET}")
            continue

        if input_type == "yesno":
            lowered = value.lower()
            if lowered in {"y", "yes"}:
                return True
            if lowered in {"n", "no"}:
                return False
            print(f"{RED}Please type yes or no.{RESET}")
            continue

        # Default fallback for unknown type request.
        return value
