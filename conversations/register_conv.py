from mark_ups import *

reg_users = {}


def check_reg(user_id):
    session = db_session.create_session()
    q = session.query(User)
    session.close()
    data = q.all()
    for elem in data:
        if elem.user_id == user_id:
            return True
    return False


async def reg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    in_data = check_reg(update.message.from_user.id)
    if not in_data:
        await update.message.reply_text(f"Начало регистрации")
        await update.message.reply_text(f"Подтвердить / Отмена", reply_markup=accept_markup)
        return 0
    else:
        await update.message.reply_text(f"Вы уже зарегистрированы", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


async def reg_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    match update.message.text:
        case "Подтвердить":
            reg_users[update.message.from_user.id] = ""
            await update.message.reply_text(f"Введите имя:", reply_markup=ReplyKeyboardRemove())
            return 1
        case "Отмена":
            return ConversationHandler.END
        case _:
            await update.message.reply_text(f"Неверный ввод", reply_markup=accept_markup)
            return 0


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(update.message.text) <= 16:
        reg_users[update.message.from_user.id] = update.message.text
        await update.message.reply_text(f"Введите Пароль:")
        return 2
    else:
        await update.message.reply_text(f"Имя должно иметь длину менее 16 символов")
        await update.message.reply_text(f"Введите имя")
        return 1


async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 8 <= len(update.message.text) <= 32:
        await update.message.reply_text(f"Регистрация завершена", reply_markup=ReplyKeyboardRemove())
        user = User()
        user.user_id = update.message.from_user.id
        user.name = reg_users[update.message.from_user.id]
        user.user_name = update.message.from_user.username
        user.set_password(password=update.message.text)
        user.balance = 0
        session = db_session.create_session()
        session.add(user)
        session.commit()
        session.close()
        return ConversationHandler.END
    else:
        await update.message.reply_text(f"Пароль должно иметь длину от 8 до 32 символов")
        await update.message.reply_text(f"Введите пароль")
        return 2


reg_handler = ConversationHandler(
    entry_points=[CommandHandler('reg', reg)],
    states={
        0: [MessageHandler(filters.TEXT, reg_check)],
        1: [MessageHandler(filters.TEXT, get_name)],
        2: [MessageHandler(filters.TEXT, get_password)]
    },
    fallbacks=[CommandHandler("cancel", stop)]
)
