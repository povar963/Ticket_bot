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
from data import db_session

accept_keyboard = [['Подтвердить'], ['Отмена']]
accept_markup = ReplyKeyboardMarkup(accept_keyboard, one_time_keyboard=False)

event_keyboard = [['Фильм'], ['Театральное представление'], ['Концерт']]
event_type_markup = ReplyKeyboardMarkup(event_keyboard, one_time_keyboard=False)

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Регистрация остановлена", reply_markup=ReplyKeyboardRemove())