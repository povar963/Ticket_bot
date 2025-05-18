from pyexpat.errors import messages
from sqlalchemy.testing.provision import drop_views
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
    CommandHandler,
)
from datetime import datetime
from config import BOT_TOKEN
from data.__all_models import User, Event_model
from mark_ups import *
from conversations.register_conv import reg_handler
from conversations.new_event_conv import event_handler
from conversations.show_events_conv import show_conv




async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Инфо")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать", reply_markup=ReplyKeyboardRemove())


def main():
    db_session.global_init("./db/data.sqlite")
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(reg_handler)

    application.add_handler(event_handler)

    application.add_handler(show_conv)

    application.add_handler(CommandHandler("start", start))

    application.run_polling()


if __name__ == '__main__':
    main()
