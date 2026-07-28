"""Production Telegram bot entrypoint using Long Polling for Background Workers."""

import asyncio
import logging
import sys
from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN, LOG_LEVEL
from database import init_db
from handlers.about import about_handler
from handlers.checker import check_command
from handlers.generator import generate_command
from handlers.help import help_handler
from handlers.passphrase import passphrase_command
from handlers.settings import settings_callback_handler, settings_handler
from handlers.start import start_handler
from services.security_tips import get_random_tips
from services.utils import escape_markdown_v2

# Configure production logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Route callback queries from inline keyboard buttons."""
    query = update.callback_query
    if not query or not query.data:
        return

    await query.answer()
    data = query.data

    if data == "btn_main_menu":
        await start_handler(update, context)
    elif data == "btn_gen_pass":
        await generate_command(update, context)
    elif data == "btn_gen_phrase":
        await passphrase_command(update, context)
    elif data == "btn_settings":
        await settings_handler(update, context)
    elif data == "btn_help":
        await help_handler(update, context)
    elif data == "btn_check_strength_info":
        await query.message.reply_text(
            "🔍 *Password Strength Checker*\n\n"
            "Send or paste any password directly in this chat to test its security strength\\.",
            parse_mode="MarkdownV2",
        )
    elif data == "btn_tips":
        tips = get_random_tips(3)
        formatted_tips = "\n\n".join(f"• {escape_markdown_v2(t)}" for t in tips)
        await query.message.reply_text(
            f"💡 *Password Security Tips*:\n\n{formatted_tips}",
            parse_mode="MarkdownV2",
        )


def main() -> None:
    """Initialize database and start long polling."""
    logger.info("Initializing database...")
    asyncio.run(init_db())

    logger.info("Building application...")
    application = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("about", about_handler))
    application.add_handler(CommandHandler("generate", generate_command))
    application.add_handler(CommandHandler("passphrase", passphrase_command))
    application.add_handler(CommandHandler("check", check_command))
    application.add_handler(CommandHandler("settings", settings_handler))
    application.add_handler(CommandHandler("tips", lambda u, c: callback_router(u, c)))

    # Inline Keyboard Callbacks
    application.add_handler(
        CallbackQueryHandler(settings_callback_handler, pattern="^toggle_")
    )
    application.add_handler(
        CallbackQueryHandler(callback_router, pattern="^btn_")
    )

    # Fallback message handler for direct password checking
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, check_command)
    )

    # Execute with long-polling
    logger.info("Starting bot in Background Worker mode (polling)...")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
