"""User preferences and settings menu handlers."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from services.database_service import DatabaseService
from services.utils import escape_markdown_v2


async def settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Render current settings and dynamic configuration options."""
    if not update.effective_user or not update.effective_message:
        return

    user_id = update.effective_user.id
    pref = await DatabaseService.get_user_preference(user_id)

    text = (
        "⚙️ *User Preferences & Generator Settings*\n\n"
        f"• *Length*: `{pref.length}` chars\n"
        f"• *Uppercase \\[A\\-Z\\]*: {'✅' if pref.use_uppercase else '❌'}\n"
        f"• *Lowercase \\[a\\-z\\]*: {'✅' if pref.use_lowercase else '❌'}\n"
        f"• *Numbers \\[0\\-9\\]*: {'✅' if pref.use_numbers else '❌'}\n"
        f"• *Symbols \\[!@\\#\\]*: {'✅' if pref.use_symbols else '❌'}\n"
        f"• *Exclude Similar*: {'✅' if pref.exclude_similar else '❌'}\n"
        f"• *Passphrase Words*: `{pref.passphrase_words}`"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                f"Length: {pref.length}", callback_data="toggle_len"
            ),
            InlineKeyboardButton(
                f"Symbols: {'ON' if pref.use_symbols else 'OFF'}", callback_data="toggle_sym"
            ),
        ],
        [
            InlineKeyboardButton(
                f"Numbers: {'ON' if pref.use_numbers else 'OFF'}", callback_data="toggle_num"
            ),
            InlineKeyboardButton(
                f"Uppercase: {'ON' if pref.use_uppercase else 'OFF'}", callback_data="toggle_upper"
            ),
        ],
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data="btn_main_menu")],
    ]

    await update.effective_message.reply_text(
        text=text,
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def settings_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline settings buttons."""
    query = update.callback_query
    if not query or not query.data or not query.from_user:
        return

    await query.answer()
    user_id = query.from_user.id
    pref = await DatabaseService.get_user_preference(user_id)

    data = query.data
    if data == "toggle_len":
        new_len = 12 if pref.length >= 32 else pref.length + 4
        await DatabaseService.update_user_preference(user_id, length=new_len)
    elif data == "toggle_sym":
        await DatabaseService.update_user_preference(user_id, use_symbols=not pref.use_symbols)
    elif data == "toggle_num":
        await DatabaseService.update_user_preference(user_id, use_numbers=not pref.use_numbers)
    elif data == "toggle_upper":
        await DatabaseService.update_user_preference(user_id, use_uppercase=not pref.use_uppercase)

    pref = await DatabaseService.get_user_preference(user_id)

    text = (
        "⚙️ *User Preferences & Generator Settings*\n\n"
        f"• *Length*: `{pref.length}` chars\n"
        f"• *Uppercase \\[A\\-Z\\]*: {'✅' if pref.use_uppercase else '❌'}\n"
        f"• *Lowercase \\[a\\-z\\]*: {'✅' if pref.use_lowercase else '❌'}\n"
        f"• *Numbers \\[0\\-9\\]*: {'✅' if pref.use_numbers else '❌'}\n"
        f"• *Symbols \\[!@\\#\\]*: {'✅' if pref.use_symbols else '❌'}\n"
        f"• *Exclude Similar*: {'✅' if pref.exclude_similar else '❌'}\n"
        f"• *Passphrase Words*: `{pref.passphrase_words}`"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                f"Length: {pref.length}", callback_data="toggle_len"
            ),
            InlineKeyboardButton(
                f"Symbols: {'ON' if pref.use_symbols else 'OFF'}", callback_data="toggle_sym"
            ),
        ],
        [
            InlineKeyboardButton(
                f"Numbers: {'ON' if pref.use_numbers else 'OFF'}", callback_data="toggle_num"
            ),
            InlineKeyboardButton(
                f"Uppercase: {'ON' if pref.use_uppercase else 'OFF'}", callback_data="toggle_upper"
            ),
        ],
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data="btn_main_menu")],
    ]

    await query.edit_message_text(
        text=text,
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
