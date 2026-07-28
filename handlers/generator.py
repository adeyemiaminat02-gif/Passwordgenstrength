"""Password generation command and callback handlers."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from services.database_service import DatabaseService
from services.password_generator import generate_password
from services.utils import escape_markdown_v2


async def generate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /generate command."""
    if not update.effective_user or not update.effective_message:
        return

    user_id = update.effective_user.id
    pref = await DatabaseService.get_user_preference(user_id)

    pwd = generate_password(
        length=pref.length,
        use_uppercase=pref.use_uppercase,
        use_lowercase=pref.use_lowercase,
        use_numbers=pref.use_numbers,
        use_symbols=pref.use_symbols,
        exclude_similar=pref.exclude_similar,
        exclude_ambiguous=pref.exclude_ambiguous,
    )

    safe_pwd = escape_markdown_v2(pwd)

    text = (
        "🎲 *Generated Secure Password*:\n\n"
        f"`{safe_pwd}`\n\n"
        "Tap the password above to copy it to your clipboard\\."
    )

    keyboard = [
        [InlineKeyboardButton("🔄 Regenerate", callback_data="btn_gen_pass")],
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data="btn_main_menu")],
    ]

    await update.effective_message.reply_text(
        text=text,
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
