import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from INFO import BOT_TOKEN
from txt_reader import reading

# Включаем логирование, чтобы отслеживать ошибки
logging.basicConfig(level=logging.INFO)

# Создаем объект бота
bot = Bot(token=BOT_TOKEN)

# Создаем объект диспетчера для обработки сообщений
dp = Dispatcher(bot)

# Список групп
groups = ['АМ-31,33', 'АМ-32,34', 'АМ-41', 'АМ-42,43', 'АС-11', 'АЭ-11', 'АЭ-21,22', 'АЭ-31,32', 'БУ-21,22',
          'БУ-31,32', 'ИС-11', 'ИС-12', 'ИС-13', 'ИС-21,23', 'ИС-22,24', 'ИС-31,34',
          'ИС-32,35', 'ИС-33,36', 'ИС-41,43', 'ИС-42,44', 'ЛЗ-11', 'ЛЗ-21,22', 'ЛЗ-31,32', 'ЛЗ-41', 'ЛП-11',
          'МЭ-11', 'МЭ-21,22', 'МЭ-31,32', 'МЭ-41,42', 'ОЛ-11', 'ОЛ-21,22', 'ОЛ-31,32',
          'ОП-11', 'ОП-21,22', 'ОП-31,32', 'ОП-41,44', 'РД-11', 'РЗ-11', 'ТД-11', 'ТД-21,22', 'ТД-31,32',
          'ТД-41,42', 'ТП-11', 'ТП-21', 'ТП-31,32', 'ТП-41', 'ЭМ-11', 'ЭМ-12', 'ЭМ-21,22',
          'ЭМ-31,32', 'ЭМ-41,43', 'ЭМ-42,44', 'ЭС-11', 'ЭС-21', 'ЭС-31,32', 'ЭС-41,42', 'ЮР-11,13', 'ЮР-12',
          'ЮР-21,23', 'ЮР-22,24', 'ЮР-25', 'ЮР-31,33', 'ЮР-32,34', 'ЮР-35,36']

# Словарь для хранения выбранных групп
selected_groups = {}


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command_handler(message: types.Message):
    """
    Обрабатываем команду /start и просим пользователя выбрать группу
    """
    await message.answer("Привет! Введи название группы (например, 'ОЛ-11' или 'ЮР-21')")


# Обработчик сообщений с названием группы
@dp.message_handler(lambda message: message.text in groups)
async def group_selected_handler(message: types.Message):
    """
    Обрабатываем сообщение с названием группы и предлагаем выбрать подгруппу
    """
    # Получаем название группы
    group_name = message.text

    # Запоминаем выбранную группу
    selected_groups[message.chat.id] = group_name

    # Создаем клавиатуру с кнопками для выбора подгруппы
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Подгруппа 1', callback_data='subgroup1')
    button2 = types.InlineKeyboardButton('Подгруппа 2', callback_data='subgroup2')
    keyboard.add(button1, button2)

    # Отправляем сообщение с выбранной группой и клавиатурой для выбора подгруппы
    await message.answer(f"Выбрана группа {group_name}. Выбери подгруппу:", reply_markup=keyboard)


# Обработчик нажатия на инлайн-кнопки
@dp.callback_query_handler(lambda c: c.data in ['subgroup1', 'subgroup2'])
async def process_callback_button(callback_query: types.CallbackQuery):
    """
    Обрабатываем нажатие на инлайн-кнопку и отвечаем сообщением с информацией о выбранной группе и подгруппе
    """
    # Получаем название выбранной подгруппы
    subgroup_name = callback_query.data


    readed_text = reading()


    # Получаем название выбранной группы из словаря
    group_name = selected_groups.get(callback_query.message.chat.id)

    # Отправляем сообщение с информацией о выбранной группе и подгруппе
    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=f"Выбрана группа {group_name}, подгруппа {subgroup_name}.")

    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=f"{readed_text}")

    # Закрываем инлайн-клавиатуру после нажатия на кнопку
    await bot.answer_callback_query(callback_query.id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
