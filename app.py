############################################################################################
#Импортирования Бота, тайпов, Диспетчера, Экзекютора, стэйтов, Токенов, Обычных и инлайновых #кнопок, Базу данных, фильтров как Текст и др мелкие
############################################################################################


from aiogram import Bot, types
from aiogram.types.message import ContentType 
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import state
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
from aiogram.utils import executor
from config import TOKEN, YOOTOKEN
import client_kb as nav
from aiogram.types import ReplyKeyboardRemove, callback_query, message
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text  
import data_base


#########################################################################
#Функия запуска, бота, Дп, Мемори хранилища и класа для Машины сотоянии##
#########################################################################


async def on_startup(_):
  print('Bot online')
  data_base.sqlite_start()


storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


class FSMAdmin(StatesGroup):
  photo = State()
  name = State()
  password = State()
  car = State()


##########################################################################
#Хендлэры Для старта, Админки и Пароля для входа в Админкку###############
##########################################################################


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
  await bot.send_message(message.from_user.id, 'Привет {0.first_name} 🖐'.format(message.from_user), reply_markup=nav.menu_adm)


@dp.message_handler(Text(equals='Админка', ignore_case=True))
async def admin_panel(message: types.Message):
  await message.reply('Введи пароль')

@dp.message_handler(lambda message: 'Азбердос' in message.text)
async def pass_true(message: types.Message):
  await bot.send_message(message.from_user.id,'Хозяин, чего надо?', reply_markup=nav.show_buy)


###################################################################################################
#Хэндлеры для Машины состояния: для Принудительной отмены, Для Купить, Фото, Пароля и Модели машины
###################################################################################################


@dp.message_handler(state="*", commands='Отменить')
@dp.message_handler(Text(equals='Отменить', ignore_case=True), state="*")
async def buy_cancel(message: types.Message, state: FSMContext):
  current_state = await state.get_state()
  if current_state is None:
    return
  await state.finish()
  await message.reply('Отмена покупки', reply_markup=nav.kb_client)


@dp.message_handler(Text(equals='Купить', ignore_case=True))
async def buy_start(message: types.Message):
  await FSMAdmin.photo.set()
  await message.reply('Для отмены покупки напишите "Отменить"\nОтправьте фото машины', reply_markup=nav.cancel_buy)


@dp.message_handler(content_types=['photo'],state=FSMAdmin.photo)
async def buy_photo(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply('Введите ваше имя')


@dp.message_handler(state=FSMAdmin.name)
async def buy_name(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['names'] = str(message.text)
    await FSMAdmin.next()
    await message.reply('Придумайте пароль')
  

@dp.message_handler(state=FSMAdmin.password)
async def buy_password(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['pass'] = message.text
    await FSMAdmin.next()
    await message.reply('Введи название модели: \nСпарк\nКобальт\nНексия\nЛасетти')


@dp.message_handler(state=FSMAdmin.car)
async def buy_car(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['cars'] = message.text
    await bot.send_message(message.from_user.id,'Ваша заявка отправлена успешно!', reply_markup=nav.payb)
  await data_base.sql_add_command(state)
  await state.finish()


#####################################################
#Колбэк квери хэндлер для оплаты через Юmoney########
#####################################################


@dp.callback_query_handler(text='оплатить')
async def submonth(call: types.CallbackQuery):
  await bot.delete_message(call.from_user.id, call.message.message_id)
  await bot.send_invoice(chat_id=call.from_user.id, title="Оплатить за машину", description="Тестовое оплата", payload="pay", provider_token=YOOTOKEN, currency="RUB", start_parameter="test_bot", prices=[{"label": "Руб", "amount": 10000}])


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
  await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=message.ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
  if message.successful_payment.invoice_payload == "pay":
    await bot.send_message(message.from_user.id, 'Поздравляю вы успешно оплатили', reply_markup=nav.menu_adm)


###########################################################################
#Пустой хэндлер для условий созданий кнопок, а также для Просмотра покупок#
###########################################################################


@dp.message_handler()
async def send_message(message: types.Message):
  if message.text == 'Меню':
    await bot.send_message(message.from_user.id, 'Список меню', reply_markup=nav.kb_client)
  elif message.text == 'Контакты':
    await message.answer('Позвонить в GM UZBEKISTAN АО вы можете по номерам:\n 78 1417777\n 71 2156871', reply_markup=nav.menu_btn)
  elif message.text == 'Отмена':
    await message.answer('Отмена действий', reply_markup=ReplyKeyboardRemove())
  elif message.text == 'Назад':
    await message.answer('Назад', reply_markup=nav.menu_adm)
  elif message.text == 'Информация о машинах':
    await message.answer('Нажмите на машину, чтобы узнать информацию о нем', reply_markup=nav.ib)
    await message.answer('Список машин:', reply_markup=nav.menu_btn)
  elif message.text == 'Отменить':
    await message.answer('Меню', reply_markup=nav.kb_client)
  elif message.text == 'Просмотр покупок':
      for ret in data_base.cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nПароль: {ret[2]}\nМашина: {ret[-1]}', reply_markup=nav.eb)


###########################################################################
#Колбэк хендлэры после нажатия кнопки "Просмотр покупок"####################
###########################################################################


@dp.callback_query_handler(text='Принять')
async def accept_btn(callback: types.CallbackQuery):
  await callback.answer('Действия принимается')


@dp.callback_query_handler(text='Отклонить')
async def accept_btn(callback: types.CallbackQuery):
  await callback.answer('Действия отклоняется')


#################################################################################
#Колбэк хэндлеры для кнопки "Информация о машинах"###############################
#################################################################################


@dp.callback_query_handler(text='Спарк')
async def spark_call(callback: types.CallbackQuery):
  await callback.answer()
  await callback.message.answer('Спарк')
  await callback.message.answer('Двигатель:	1.0 МТ\nНоминальная мощность:	68 л.с./ 50 кВ @ 6400 Об/мин\nКрутящий момент: 89 Н*м/4800 Об/мин\nМаксимальная скорость:	151\nРазгон 0-100 км/ч (сек.):	15.3', reply_markup=nav.menu_btn)


@dp.callback_query_handler(text='Кобальт')
async def spark_call(callback: types.CallbackQuery):
  await callback.answer()
  await callback.message.answer('Кобальт')
  await callback.message.answer('Двигатель, л:	1.5 МТ(АТ)\nМакс. мощность кВт (или л.с.) при ... оборотах/мин:	105/5800\nМакс. крутящий момент Нм при ... оборотах/мин:	134/4000\nСнаряженная масса, кг:	1590', reply_markup=nav.menu_btn)


@dp.callback_query_handler(text='Нексиа')
async def spark_call(callback: types.CallbackQuery):
  await callback.answer()
  await callback.message.answer('Нексиа')
  await callback.message.answer('Название:	Nexia DOHC\nСнаряженная масса автомобиля, кг, кг.:	1190/1230\nМаксимальная скорость, км/ч, км/ч:	178/179\nРазгон до 100 км/ч с места, cекунд, с:	12,2/12,3', reply_markup=nav.menu_btn)


@dp.callback_query_handler(text='Ласетти')
async def spark_call(callback: types.CallbackQuery):
  await callback.answer()
  await callback.message.answer('Ласетти')
  await callback.message.answer('Название комплектации:	1.8 AT CDX\nМаксимальная мощность, л.с. (кВт) при об./мин.:	122 (90) / 5800\nМаксимальный крутящий момент, Н*м (кг*м) при об./мин.:	165 (17) / 4000\nУдельная мощность, кг/л.с.:	9.59', reply_markup=nav.menu_btn)


#######################################################################################
#Ну и сам экзекютор чтобы активировать dp, стартовое сообщение и пропустить обновления#
#######################################################################################


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)