from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Токен бота (вставь свой!)
import os
TOKEN = os.getenv(8164069115:AAHPX5iqw5rGbH_WNisMpCb5XsXZa3Wh7qU)

# Username администратора (куда отправлять данные)
ADMIN_ID = 5713965537  # заменить на @username администратора

# Состояния для сбора данных
USER_STATE = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я бот центра. Вот список команд:\n"
        "/start — начать\n"
        "/price — стоимость занятий\n"
        "/center — информация о центре\n"
        "/demo — записаться на пробное занятие\n"
        "/zam — запись на замещение\n"
        "/mp — ближайшие мероприятия"
    )

# Команда /price
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Первое занятие бесплатное.\n"
        "Далее:\n"
        "• 1 раз в неделю — 5.600 руб.\n"
        "• 2 раза в неделю — 8.700 руб."
    )
    await update.message.reply_text(text)

# Команда /center
async def center(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        Откройте для своего ребёнка увлекательное путешествие в мир английского языка с курсами Helen Doron, где обучение строится на радости, игре и уверенности: более 3 миллионов довольных учеников по всему миру подтверждают эффективность уникальной методики, при которой дети от 3 месяцев до 19 лет естественным образом усваивают язык через песни, игры, творчество и более 20 структурированных курсов, соответствующих возрасту и уровню, погружаясь в языковую среду не только на уроках, но и дома с помощью специальных аудио и приложений — создавая прочную основу для свободного владения английским как вторым родным языком.
    )
    await update.message.reply_text(text)

# Команда /demo — начало заполнения формы
async def demo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_user.id
    USER_STATE[chat_id] = {"form": "demo"}
    keyboard = [[KeyboardButton("Отмена")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "Чтобы записаться на пробное занятие, заполните поля ниже:\n\n"
        "Имя и фамилия ребенка:",
        reply_markup=reply_markup
    )

# Команда /zam — начало заполнения формы
async def zam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_user.id
    USER_STATE[chat_id] = {"form": "zam"}
    keyboard = [[KeyboardButton("Отмена")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "Чтобы записаться на замещение пропущенного занятия, заполните поля ниже:\n\n"
        "Имя и фамилия ребенка:",
        reply_markup=reply_markup
    )

# Команда /mp
async def mp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Ближайшие мероприятия:\n\n• 25 октября в 17:00- Хэллоуин(10+ лет) \n• 28 октября- мероприятие "Япония""
    await update.message.reply_text(text)

# Обработка текста (для форм)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_user.id
    text = update.message.text

    if text == "Отмена":
        USER_STATE.pop(chat_id, None)
        await update.message.reply_text("Форма отменена.", reply_markup=ReplyKeyboardMarkup([], one_time_keyboard=True))
        return

    if chat_id in USER_STATE:
        form_data = USER_STATE[chat_id]

        if form_data["form"] == "demo":
            if "name" not in form_data:
                form_data["name"] = text
                await update.message.reply_text("Возраст ребенка (в годах и месяцах):")
            elif "age" not in form_data:
                form_data["age"] = text
                await update.message.reply_text("Номер телефона, по которому можно обратиться:")
            elif "phone" not in form_data:
                form_data["phone"] = text

                # Отправляем данные админу
                admin_text = (
                    "ДЕМО\n"
                    f"Имя и фамилия: {form_data['name']}\n"
                    f"Возраст: {form_data['age']}\n"
                    f"Телефон: {form_data['phone']}\n"
                    f"От: @{update.effective_user.username or update.effective_user.first_name}"
                )
                try:
                    admin_user = await context.bot.get_chat(ADMIN_ID)
                    await context.bot.send_message(chat_id=admin_user.id, text=admin_text)
                    await update.message.reply_text(
                        "✅ Спасибо! Данные отправлены администратору. С вами свяжутся в ближайшее время."
                    )
                except Exception as e:
                    print(f"Ошибка при отправке администратору: {e}")
                    await update.message.reply_text(
                        f"❌ Ошибка при отправке: {str(e)}\n\nПожалуйста, сообщите администратору."
                    )

                USER_STATE.pop(chat_id, None)

        elif form_data["form"] == "zam":
            form_data["name"] = text
            # Отправляем данные админу
            admin_text = (
                "ЗАМЕНА\n"
                f"Имя и фамилия: {form_data['name']}\n"
                f"От: @{update.effective_user.username or update.effective_user.first_name}"
            )
            try:
                admin_user = await context.bot.get_chat(ADMIN_ID)
                await context.bot.send_message(chat_id=admin_user.id, text=admin_text)
                await update.message.reply_text(
                    "✅ Спасибо! Данные отправлены администратору."
                )
            except Exception as e:
                print(f"Ошибка при отправке администратору: {e}")
                await update.message.reply_text(
                    f"❌ Ошибка при отправке: {str(e)}\n\nПожалуйста, сообщите администратору."
                )

            USER_STATE.pop(chat_id, None)
    else:
        await update.message.reply_text("Я не понимаю. Напиши /start, чтобы увидеть команды.")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("center", center))
    application.add_handler(CommandHandler("demo", demo))
    application.add_handler(CommandHandler("zam", zam))
    application.add_handler(CommandHandler("mp", mp))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен!")
    application.run_polling()

if __name__ == '__main__':
    main()