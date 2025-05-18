from mark_ups import *

event_users = {0: {
    "type": "",
    "name": "",
    "date_time": "",
    "description": "",
    "cost": ""
}
}


async def create_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Вы хотите организовать событие?")
    await update.message.reply_text(f"Подтвердить / Отмена", reply_markup=accept_markup)
    return 0


async def check_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    match update.message.text:
        case "Подтвердить":
            event_users[update.message.from_user.id] = {}
            await update.message.reply_text(f"Введите тип:", reply_markup=event_type_markup)
            return 1
        case "Отмена":
            await update.message.reply_text(f"Действие отменено", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        case _:
            await update.message.reply_text(f"Неверный ввод", reply_markup=accept_markup)
            return 0


async def get_event_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text in ["Фильм", "Театральное представление", "Концерт"]:
        event_users[update.message.from_user.id]["type"] = update.message.text
        await update.message.reply_text(f"Введите название:", reply_markup=ReplyKeyboardRemove())
        return 2
    else:
        await update.message.reply_text(f"Выберите тип из предложенных ниже", reply_markup=event_type_markup)
        return 1


async def get_event_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(update.message.text) <= 32:
        event_users[update.message.from_user.id]["name"] = update.message.text
        await update.message.reply_text(f"Введите описание", reply_markup=ReplyKeyboardRemove())
        return 3
    else:
        await update.message.reply_text(f"Название события должно иметь длину менее 32 символов")
        await update.message.reply_text(f"Введите Название:")
        return 2


async def get_event_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(update.message.text) <= 256:
        event_users[update.message.from_user.id]["description"] = update.message.text
        await update.message.reply_text(f"Введите дату (пример '31.12.25 23:59'):", reply_markup=ReplyKeyboardRemove())
        return 4
    else:
        await update.message.reply_text(f"Описание должно иметь длину менее 256 символов")
        await update.message.reply_text(f"Введите описание")
        return 3


async def get_event_datetime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    datetime = update.message.text
    try:
        date = datetime.split(" ")
        time, date = date[1].split(":"), date[0].split(".")
        event_users[update.message.from_user.id]["date_time"] = datetime
        await update.message.reply_text(f"Введите сумму")
        return 5
    except IndexError:
        await update.message.reply_text(f"Дата должна соответствовать примеру - '31.12.25 23:59'")
        await update.message.reply_text(f"Введите дату:")
        return 4


async def get_cost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        cost = int(update.message.text)
        event_users[update.message.from_user.id]["cost"] = cost
        message = f"""Вы хотите устроить {event_users[update.message.from_user.id]['type']}
имя: {event_users[update.message.from_user.id]['name']}
дата: {event_users[update.message.from_user.id]['date_time']}
описание: {event_users[update.message.from_user.id]['description']}
Стоимость: {cost}
"""
        await update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
        await update.message.reply_text(f"Введите Подтвердить/Отменить", reply_markup=accept_markup)
        return 6
    except ValueError:
        await update.message.reply_text(f"Сумма указана неверно", reply_markup=accept_markup)
        return 5


def get_author_id(user_id):
    session = db_session.create_session()
    q = session.query(User).filter(User.user_id == user_id)
    session.close()
    data = q.all()
    return data[0].id


async def accept_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    match update.message.text:
        case "Подтвердить":
            event = Event_model()
            event.cost = event_users[update.message.from_user.id]['cost']
            event.type = event_users[update.message.from_user.id]['type']
            event.name = event_users[update.message.from_user.id]['name']
            event.description = event_users[update.message.from_user.id]['description']
            event.users = 0
            event.author_user_id = update.message.from_user.id
            event.author_id = get_author_id(update.message.from_user.id)
            event.date_time = event_users[update.message.from_user.id]["date_time"]
            session = db_session.create_session()
            session.add(event)
            session.commit()
            session.close()
            await update.message.reply_text(f"Событие создано", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        case "Отмена":
            await update.message.reply_text(f"Процесс остановлен", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        case _:
            await update.message.reply_text(f"Неверный ввод", reply_markup=accept_markup)
            return 6


event_handler = ConversationHandler(
    entry_points=[CommandHandler('create_event', create_event)],
    states={
        0: [MessageHandler(filters.TEXT, check_event)],
        1: [MessageHandler(filters.TEXT, get_event_type)],
        2: [MessageHandler(filters.TEXT, get_event_name)],
        3: [MessageHandler(filters.TEXT, get_event_description)],
        4: [MessageHandler(filters.TEXT, get_event_datetime)],
        5: [MessageHandler(filters.TEXT, get_cost)],
        6: [MessageHandler(filters.TEXT, accept_event)],
    },
    fallbacks=[CommandHandler("cancel", stop)]
)
