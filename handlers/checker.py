"""Password strength analysis command handler."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from services.strength_checker import analyze_password
from services.utils import escape_markdown_v2, sanitize_input


async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle explicit /check command or direct text input."""
    if not update.effective_message:
        return

    message_text = update.effective_message.text or ""

    if message_text.startswith("/check"):
        parts = message_text.split(maxsplit=1)
        if len(parts) < 2:
            await update.effective_message.reply_text(
                "❌ Please specify a password to check\\.\n*Usage*: `/check MyPassword123\\!`",
                parse_mode="MarkdownV2",
            )
            return
        pwd = parts[1]
    else:
        pwd = message_text

    pwd = sanitize_input(pwd)
    result = analyze_password(pwd)

    rating_emoji = {
        "Very Weak": "🔴",
        "Weak": "🟠",
        "Fair": "🟡",
        "Good": "🟢",
        "Strong": "🔵",
        "Very Strong": "👑",
    }.get(result["rating"], "❓")

    recs = "\n".join(f"• {escape_markdown_v2(r)}" for r in result["recommendations"])

    response = (
        "📊 *Password Strength Analysis*\n\n"
        f"*Rating*: {rating_emoji} {escape_markdown_v2(result['rating'])}\n"
        f"*Score*: `{result['numerical_score']}/100`\n"
        f"*Entropy*: `{result['entropy']} bits`\n"
        f"*Est\\. Crack Time*: `{escape_markdown_v2(result['crack_time'])}`\n\n"
        "💡 *Recommendations*:\n"
        f"{recs}"
    )

    # Attempt to delete the user's plain text password message for privacy
    try:
        await update.effective_message.delete()
    except Exception:
        pass

    keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data="btn_main_menu")]]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
