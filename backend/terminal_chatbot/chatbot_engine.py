"""Keyword-based chatbot response engine."""

from __future__ import annotations

import random
from typing import Dict, List


class ChatbotEngine:
    """Simple deterministic-ish keyword chatbot with fallback responses."""

    def __init__(self) -> None:
        self.keyword_responses: Dict[str, str] = {
            "hello": "Hello! Nice to meet you. How can I help today?",
            "hi": "Hi there! What can I help you with?",
            "help": "I can help with account settings, pricing questions, and basic troubleshooting.",
            "pricing": "We offer Starter, Growth, and Scale plans. Tell me your team size and I can suggest one.",
            "price": "Pricing depends on your usage and team size. Want a quick plan recommendation?",
            "support": "I can help troubleshoot. Please share what you were trying to do and any error message.",
            "error": "Sorry you hit an error. Share the exact error text and when it happens.",
            "login": "If login fails, verify your username/password and check caps lock.",
            "signup": "To sign up, choose a unique username and a strong password of at least 8 characters.",
            "history": "Your chat history is saved locally for your account and can be cleared from Privacy settings.",
            "privacy": "You can view, clear, or delete your data from the privacy menu.",
            "thanks": "You're welcome! If you'd like, I can help with one more thing.",
            "bye": "Goodbye! Have a great day.",
        }
        self.fallback_responses: List[str] = [
            "I didn't fully catch that. Try asking about pricing, support, login, or privacy.",
            "Could you rephrase that? I can help with account, support, and plan questions.",
            "I'm still learning. Try keywords like help, pricing, history, or error.",
        ]

    def get_response(self, user_input: str) -> str:
        """Generate a response based on matched keywords.

        Matching is case-insensitive and supports multiple keywords in one input.
        """
        text = (user_input or "").strip().lower()
        if not text:
            return "Please type a message so I can help you."

        matched = []
        for keyword, response in self.keyword_responses.items():
            if keyword in text:
                matched.append(response)

        if matched:
            # Preserve order and remove duplicates for a cleaner response.
            unique_parts = list(dict.fromkeys(matched))
            return "\n".join(unique_parts)

        return random.choice(self.fallback_responses)
