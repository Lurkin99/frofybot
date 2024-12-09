import telebot
from telebot import types

API_TOKEN = '7642894929:AAErc1k42W3_iCsX3aMchpti-pIlM-Ij_sY'
bot = telebot.TeleBot(API_TOKEN)

admin_id = 5749521046  # ID администратора

# Список пользователей
users = [5749521046]  # Сюда добавляйте ID пользователей, которые начали взаимодействовать с ботом

# Хранение кнопок и их сообщений
custom_buttons = {}
start_message = "💎добро пожаловать в магазин для покупки телеграм премиума💎"  # Изначальное сообщение, которое будет отправляться при запуске

# Предустановленные кнопки, которые будут отображаться при вызове /start
preset_buttons = {
    "🛒Каталог подписок": "premium_catalog",
    "📜Правила покупки": "https://telegra.ph/Pravila-pokupki-12-08-2"
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.id not in users:
        users.append(message.from_user.id)

    sticker_id = 'CAACAgIAAxkBAAKPh2dV7zdq_20aPaMmupBu9YK6lmL1AAJMXwACEXSwSohDkpKt9mK3NgQ'
    bot.send_sticker(message.chat.id, sticker_id)

    keyboard = types.InlineKeyboardMarkup()
    
    # Добавляем все пользовательские кнопки в клавиатуру
    for name, text in custom_buttons.items():
        keyboard.add(types.InlineKeyboardButton(name, callback_data='custom_message:' + name))
    
    # Добавляем предустановленные кнопки
    for name, callback_data in preset_buttons.items():
        if callback_data.startswith('http'):
            keyboard.add(types.InlineKeyboardButton(name, url=callback_data))
        else:
            keyboard.add(types.InlineKeyboardButton(name, callback_data=callback_data))

    bot.send_message(message.chat.id, start_message, reply_markup=keyboard)

@bot.message_handler(commands=['adminlurkink'])
def admin_lurkink(message):
    if message.from_user.id == admin_id:
        bot.send_message(message.chat.id, "Вы попали в меню для админа")
        
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Изменить сообщение /start", callback_data='edit_start_message'))
        keyboard.add(types.InlineKeyboardButton("Ввести сообщение для рассылки", callback_data='input_message'))
        keyboard.add(types.InlineKeyboardButton("Создать кнопку", callback_data='create_button'))
        keyboard.add(types.InlineKeyboardButton("Удалить кнопку", callback_data='delete_button'))

        bot.send_message(message.chat.id, "Пожалуйста, выберите действие.", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Вы не являетесь администратором.")

@bot.callback_query_handler(func=lambda call: call.data == 'edit_start_message')
def prompt_edit_start_message(call):
    bot.send_message(call.message.chat.id, "Введите новое сообщение для команды /start:")
    bot.register_next_step_handler(call.message, process_edit_start_message)

def process_edit_start_message(message):
    global start_message
    start_message = message.text
    bot.send_message(message.chat.id, f"Сообщение для /start было изменено на:\n{start_message}")

@bot.callback_query_handler(func=lambda call: call.data == 'delete_button')
def prompt_delete_button(call):
    keyboard = types.InlineKeyboardMarkup()
    # Добавляем пользовательские кнопки для удаления
    for name in custom_buttons.keys():
        keyboard.add(types.InlineKeyboardButton(name, callback_data='confirm_delete:' + name))
    
    # Добавляем предустановленные кнопки для удаления
    
    keyboard.add(types.InlineKeyboardButton("Каталог премиумов", callback_data='confirm_delete:premium_catalog'))
    keyboard.add(types.InlineKeyboardButton("Правила покупки", callback_data='confirm_delete:rules'))

    keyboard.add(types.InlineKeyboardButton("Назад", callback_data='admin_menu'))
    bot.send_message(call.message.chat.id, "Выберите кнопку для удаления:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_delete:'))
def confirm_delete(call):
    button_name = call.data.split(':', 1)[1]
    if button_name in custom_buttons:
        del custom_buttons[button_name]
        bot.send_message(call.message.chat.id, f"Кнопка '{button_name}' была удалена!")
        update_start_keyboard()  # Обновляем клавиатуру после удаления кнопки
    elif button_name == 'premium_catalog':
        bot.send_message(call.message.chat.id, "Предустановленная кнопка 'Каталог премиумов' не может быть удалена.")
    elif button_name == 'rules':
        bot.send_message(call.message.chat.id, "Предустановленная кнопка 'Правила покупки' не может быть удалена.")
    else:
        bot.send_message(call.message.chat.id, "Кнопка не найдена.")

@bot.callback_query_handler(func=lambda call: call.data == 'admin_menu')
def show_admin_menu(call):
    admin_lurkink(call.message)

@bot.callback_query_handler(func=lambda call: call.data == 'input_message')
def prompt_for_message(call):
    bot.send_message(call.message.chat.id, "Пожалуйста, введите сообщение для рассылки.(не работает)")
    bot.register_next_step_handler(call.message, process_message_input)

def process_message_input(message):
    text_to_broadcast = message.text
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Да", callback_data='confirm_broadcast:' + text_to_broadcast), 
                 types.InlineKeyboardButton("Нет", callback_data='cancel_broadcast'))

    bot.send_message(message.chat.id, "Вы желаете сделать рассылку?(не работает)", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'create_button')
def start_create_button(call):
    bot.send_message(call.message.chat.id, "Введите название кнопки:")
    bot.register_next_step_handler(call.message, process_button_name)

def process_button_name(message):
    button_name = message.text
    bot.send_message(message.chat.id, "Теперь введите сообщение, которое будет отправлено при нажатии на кнопку:")
    bot.register_next_step_handler(message, process_button_message, button_name)

def process_button_message(message, button_name):
    message_text = message.text
    
    # Сохраняем кнопку и ее сообщение в словаре
    custom_buttons[button_name] = message_text

    bot.send_message(message.chat.id, f"Кнопка '{button_name}' создана!")
    update_start_keyboard()  # Обновляем клавиатуру при создании кнопки

@bot.callback_query_handler(func=lambda call: call.data.startswith('custom_message:'))
def handle_custom_message(call):
    button_name = call.data.split(':', 1)[1]
    message_text = custom_buttons.get(button_name, "Это сообщение не найдено.")
    bot.send_message(call.message.chat.id, message_text)

def update_start_keyboard():
    # Обновляем стартовую клавиатуру для всех пользователей
    for user_id in users:
        try:
            # Создаем новую клавиатуру с кнопками
            keyboard = types.InlineKeyboardMarkup()

            # Добавляем все пользовательские кнопки
            for name, text in custom_buttons.items():
                keyboard.add(types.InlineKeyboardButton(name, callback_data='custom_message:' + name))

            # Добавляем предустановленные кнопки
            for name, callback_data in preset_buttons.items():
            	
                if callback_data.startswith('http'):
                    keyboard.add(types.InlineKeyboardButton(name, url=callback_data))
                else:
                    keyboard.add(types.InlineKeyboardButton(name, callback_data=callback_data))

            bot.send_message(user_id, start_message, reply_markup=keyboard)
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_broadcast:'))
def confirm_broadcast(call):
    text_to_broadcast = call.data.split(':', 1)[1]
    bot.send_message(call.message.chat.id, "Начинаю рассылку!(не работает)")

    for user_id in users:
        try:
            bot.send_message(user_id, text_to_broadcast)
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

@bot.callback_query_handler(func=lambda call: call.data == 'cancel_broadcast')
def cancel_broadcast(call):
    bot.send_message(call.message.chat.id, "Рассылка отменена.")

@bot.callback_query_handler(func=lambda call: call.data == 'premium_catalog')
def send_catalog(call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("⭐1 месяц", callback_data='1_month'), 
                 types.InlineKeyboardButton("💫3 месяца", callback_data='3_month'))
    keyboard.add(types.InlineKeyboardButton("🌟6 месяцев", callback_data='6_month'), 
                 types.InlineKeyboardButton("✨12 месяцев", callback_data='12_month'))

    bot.send_message(call.message.chat.id, "🛒Каталог подписок телеграм премиум🛒", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['1_month', '3_month', '6_month', '12_month'])
def handle_premium_month(call):
    month = call.data
    price_info = {
        '1_month': """🛒Товар: премиум 1 месяц.
\n💰Цена: 4$/400₽\n
🔗Ссылка на оплату: http://t.me/send?start=IVWPEvN98HG7""",
        '3_month': """🛒Товар: премиум 3 месяца.
\n💰Цена: 14$/1400₽\n
🔗Ссылка на оплату: http://t.me/send?start=IVl3EY9mJwSg""",
        '6_month': """🛒Товар: премиум 6 месяцев.
\n💰Цена: 18.5$/1850₽\n
🔗Ссылка на оплату: http://t.me/send?start=IVLWTYiOb2Ix""",
        '12_month': "🛒Выберите способ получения"
    }

    if month in price_info:
        if month == '12_month':
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton("💳Карта", callback_data='payment_card'))
            keyboard.add(types.InlineKeyboardButton("🎁Гифт", callback_data='payment_gift'))
            bot.send_message(call.message.chat.id, price_info[month], reply_markup=keyboard)
        else:
            bot.send_message(call.message.chat.id, price_info[month] + ".", reply_markup=create_payment_keyboard())
    else:
        bot.send_message(call.message.chat.id, "📛Неизвестный товар.")

@bot.callback_query_handler(func=lambda call: call.data == 'payment_card')
def handle_payment_card(call):
    # Отправляем пользователю ссылку на оплату через карту
    payment_link = "http://t.me/send?start=IVhnsslbUzQ1"
    keyboard = create_payment_keyboard()  # Добавляем кнопку "Я оплатил"
    bot.send_message(call.message.chat.id, f"""🛒Товар: премиум 12 месяцев.
\n💰Цена: 25$/2500₽\n
🔗Ссылка на оплату: {payment_link}""", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'payment_gift')
def handle_payment_gift(call):
    # Отправляем пользователю ссылку на оплату через гифт
    payment_link = "http://t.me/send?start=IVoC5DHDieyP"
    keyboard = create_payment_keyboard() 
    bot.send_message(call.message.chat.id, f"""🛒Товар: премиум 12 месяца.
\n💰Цена: 33$/3300₽\n
🔗Ссылка на оплату: {payment_link}""", reply_markup=keyboard)
    
@bot.callback_query_handler(func=lambda call: call.data == 'paid')
def handle_paid(call):
    bot.send_message(call.message.chat.id, "❗Чтобы получить премиум, обратитесь к @frofy")

def create_payment_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("💸Я оплатил", callback_data='paid'))
    return keyboard

if __name__ == '__main__':
    bot.polling(none_stop=True)