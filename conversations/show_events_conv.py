from sqlalchemy.sql.base import elements

from conversations.new_event_conv import create_event
from mark_ups import *

users_list = {
    "user_id": {
        "event_id" : ""
    }
}


async def check_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Подтвердите действие", reply_markup=accept_markup)
    return 0


async def events_show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    match update.message.text:
        case "Подтвердить":
            session = db_session.create_session()
            q = session.query(Event_model)
            session.close()
            data = q.all()
            events = []
            if len(data) != 0:
                for elem in data:
                    events.append([f"{elem.id}: {elem.name}"])
            events_keyboard = ReplyKeyboardMarkup(events, one_time_keyboard=False)
            await update.message.reply_text(f"Вот список событий", reply_markup=events_keyboard)
            return 1
        case _:
            await update.message.reply_text(f"Действие отменено", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END


def create_info(elem, session) -> str:
    q = session.query(User).filter(User.user_id == elem.author_user_id)
    data = q.all()
    if len(data) == 1:
        text = f"""
Событие: {elem.type}
Имя: {elem.name}
Время: {elem.date_time}
Проводит: {data[0].name}
Описание: {elem.description}
Стоимость: {elem.cost} (ваш баланс: {data[0].balance})
"""
    else:
        text = f"""
Событие: {elem.type}
Имя: {elem.name}
Время: {elem.date_time}
Проводит: Неизвестно
Описание: {elem.description}
Стоимость: {elem.cost} (ваш баланс: {data[0].balance})
"""
    return text


async def choose_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = db_session.create_session()
    ev_id, ev_name = update.message.text.split(": ")
    q = session.query(Event_model).filter(Event_model.id == ev_id, Event_model.name == ev_name)
    session.close()
    data = q.all()
    if len(data) == 1:
        text = create_info(data[0], session)
        await update.message.reply_text(text, reply_markup=accept_markup)
        users_list[update.message.from_user.id] = {}
        users_list[update.message.from_user.id]["event_id"] = ev_id
        users_list[update.message.from_user.id]["event_name"] = ev_name
        return 2
    else:
        await update.message.reply_text("Неверный ввод", reply_markup=ReplyKeyboardRemove())
        return 0


async def buy_ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    match update.message.text:
        case "Подтвердить":
            session = db_session.create_session()
            ev_id = users_list[update.message.from_user.id]["event_id"]
            ev_name = users_list[update.message.from_user.id]["event_name"]
            e = session.query(Event_model).filter(Event_model.id == ev_id, Event_model.name == ev_name)
            u = session.query(User).filter(User.user_id == update.message.from_user.id)
            event = e.all()[0]
            user = u.all()[0]
            if event.cost <= user.balance:
                user.balance = user.balance - event.cost
                await update.message.reply_text("Билет успешно куплен", reply_markup=ReplyKeyboardRemove())
                session.commit()
            else:
                await update.message.reply_text("У вас недостаточно денег", reply_markup=ReplyKeyboardRemove())
            session.close()
        case "Отмена":
            await update.message.reply_text("Покупка остановлена", reply_markup=ReplyKeyboardRemove())
        case _:
            await update.message.reply_text("Неверный ввод", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


show_conv = ConversationHandler(
    entry_points=[CommandHandler('events', check_events)],
    states={
        0: [MessageHandler(filters.TEXT, events_show)],
        1: [MessageHandler(filters.TEXT, choose_event)],
        2: [MessageHandler(filters.TEXT, buy_ticket)],
    },
    fallbacks=[CommandHandler("cancel", stop)]
)
