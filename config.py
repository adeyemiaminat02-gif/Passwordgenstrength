"""Application configuration module."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
BOT_USERNAME: str = os.getenv("BOT_USERNAME", "Passwordgenstrengthbot")
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data/bot.db")
DEFAULT_PASSWORD_LENGTH: int = int(os.getenv("DEFAULT_PASSWORD_LENGTH", "16"))
DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "en")
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "")
PORT: int = int(os.getenv("PORT", "8080"))

if not BOT_TOKEN:
    raise ValueError("CRITICAL: BOT_TOKEN is missing in environment variables!")
