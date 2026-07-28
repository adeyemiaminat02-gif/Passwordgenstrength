"""/about command handler."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /about command."""
    if not update.effective_message:
        return

    about_text = (
        "ℹ️ *About @Passwordgenstrengthbot*\n\n"
        "Built with Python 3\\.12, `python-telegram-bot` v22, and industrial\\-grade cryptographic primitives\\.\n\n"
        "🛡️ *Zero\\-Knowledge Privacy Policy*:\n"
        "• Passwords are evaluated strictly in\\-memory and immediately garbage-collected\\.\n"
        "• Zero logging or database persistence of credentials\\.\n"
        "• Uses `secrets` for CSPRNG random generation\\.\n\n"
        "🌐 *Open Source*: Designed for hosting on GitHub and Render\\."
    )

    keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data="btn_main_menu")]]

    await update.effective_message.reply_text(
        text=about_text,
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
