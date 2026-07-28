"""Passphrase generation command handler."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from services.database_service import DatabaseService
from services.passphrase_generator import generate_passphrase
from services.utils import escape_markdown_v2


async def passphrase_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /passphrase command."""
    if not update.effective_user or not update.effective_message:
        return

    user_id = update.effective_user.id
    pref = await DatabaseService.get_user_preference(user_id)

    phrase = generate_passphrase(
        num_words=pref.passphrase_words,
        separator=pref.passphrase_separator,
    )

    safe_phrase = escape_markdown_v2(phrase)

    text = (
        "📝 *Generated Passphrase*:\n\n"
        f"`{safe_phrase}`\n\n"
        "Tap the passphrase above to copy it\\."
    )

    keyboard = [
        [InlineKeyboardButton("🔄 Regenerate", callback_data="btn_gen_phrase")],
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data="btn_main_menu")],
    ]

    await update.effective_message.reply_text(
        text=text,
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
