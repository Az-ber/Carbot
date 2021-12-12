#######################################
#Импорт Обычных и инлайновых клавиатур#
#######################################


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup 


############################################################################
#Создание Обычных кнопок
############################################################################


b1 = KeyboardButton('Меню✨')
b2 = KeyboardButton('Информация о машинах👁‍🗨')
b3 = KeyboardButton('Отмена⛔')
b4 = KeyboardButton('Контакты📬')
b6 = KeyboardButton('Купить')
b7 = KeyboardButton('Просмотр покупок🎁')
b8 = KeyboardButton('Админка😎')
b9 = KeyboardButton('Назад🔽')
b10 = KeyboardButton('Отменить⛔')


#####################################################################
#Параметры обычных кнопок, а также объединения их
#####################################################################

cancel_buy = ReplyKeyboardMarkup(resize_keyboard=True)
menu_adm = ReplyKeyboardMarkup(resize_keyboard=True)
show_buy = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menu_btn = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_btn = ReplyKeyboardMarkup(resize_keyboard=True)
buy_btn = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b6).add(b2).insert(b4).add(b9).add(b3)
menu_btn.add(b1).add(b3)
menu_adm.add(b1).add(b8).add(b3)
show_buy.add(b7).add(b1).add(b3)
cancel_buy.add(b10)


#######################################################################################
#Создание инлайн клавиаутуры и объединения их
#######################################################################################

ib = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Спарк🚕', callback_data='Спарк🚕')).add(
    InlineKeyboardButton(text='Кобальт🚗', callback_data='Кобальт🚗')).add(InlineKeyboardButton(text='Нексиа🚖', callback_data='Нексиа🚖')).add(InlineKeyboardButton(text='Ласетти🚘', callback_data='Ласетти🚘'))

eb = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Принять✅', callback_data='Принять✅'), InlineKeyboardButton(text='Отклонить❌', callback_data='Отклонить❌'))

payb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Оплатить 100 руб🤑', callback_data='оплатить🤑'))



