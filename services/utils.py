"""General utilities for formatting and security helpers."""

import re


def escape_markdown_v2(text: str) -> str:
    """Escape special characters required for Telegram MarkdownV2 formatting."""
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", str(text))


def sanitize_input(text: str) -> str:
    """Sanitize incoming user text inputs to prevent prompt exploits/spam."""
    if not text:
        return ""
    return text.strip()[:128]
