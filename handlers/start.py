"""/start command handler."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from services.database_service import DatabaseService
from services.utils import escape_markdown_v2


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    if not update.effective_user or not update.effective_message:
        return

    user_id = update.effective_user.id
    first_name = escape_markdown_v2(update.effective_user.first_name)
    await DatabaseService.get_user_preference(user_id)

    welcome_text = (
        f"👋 *Welcome, {first_name}\\!*\n\n"
        "I am *@Passwordgenstrengthbot*, your secure password generator and security analyzer\\.\n\n"
        "🔒 *Privacy Commitment*: This bot *never* stores, logs, or transmits your passwords\\.\n\n"
        "Choose an action below or send a password directly to test its strength\\:"
    )

    keyboard = [
        [
            InlineKeyboardButton("🎲 Generate Password", callback_data="btn_gen_pass"),
            InlineKeyboardButton("📝 Generate Passphrase", callback_data="btn_gen_phrase"),
        ],
        [
            InlineKeyboardButton("🔍 Check Strength", callback_data="btn_check_strength_info"),
            InlineKeyboardButton("💡 Security Tips", callback_data="btn_tips"),
        ],
        [
            InlineKeyboardButton("⚙️ Settings", callback_data="btn_settings"),
            InlineKeyboardButton("ℹ️ Help", callback_data="btn_help"),
        ],
    ]

    await update.effective_message.reply_text(
        text=welcome_text,
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
