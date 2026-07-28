"""/help command handler."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    if not update.effective_message:
        return

    help_text = (
        "📖 *Bot Commands & Instructions*\n\n"
        "• `/start` \\- Start the bot and view the primary menu\\.\n"
        "• `/generate` \\- Generate a secure, customizable random password\\.\n"
        "• `/passphrase` \\- Generate a memorable word\\-based passphrase\\.\n"
        "• `/check <password>` \\- Analyze the security strength of a password\\.\n"
        "• `/tips` \\- View crucial password security best practices\\.\n"
        "• `/settings` \\- Adjust default generator parameters\\.\n"
        "• `/about` \\- Technical and privacy information\\.\n\n"
        "💡 *Quick Tip*: You can directly type or paste any password in chat to evaluate its strength instantly\\."
    )

    keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data="btn_main_menu")]]

    await update.effective_message.reply_text(
        text=help_text,
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
