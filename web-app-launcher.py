#!/usr/bin/env python3
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

from config import TOKEN, URL

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [InlineKeyboardButton("Сканировать QR-код", web_app=WebAppInfo(url=URL))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "Привет! Это - бот МТП для шеринга зонтов." \
           "\nДля того, чтобы взять зонт, отсканируй QR-код на зонте с помощью мини-приложения." \
           "\nДля того, чтобы вернуть зонт, отсканируй QR-код на точке выдачи зонтов с помощью мини-приложения." \
           "\nОставить отзыв или сообщить об ошибках в работе можно в мини-приложении." \
           "\nЧтобы открыть мини-приложение, нажми на кнопку ниже"

    await update.message.reply_text(text, reply_markup=reply_markup)


async def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")


async def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Type /start and open the QR dialog.")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

