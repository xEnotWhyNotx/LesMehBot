import logging
import asyncio
from INFO import BOT_TOKEN
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor


# Включаем логирование, чтобы отслеживать ошибки
logging.basicConfig(level=logging.INFO)

# Создаем объект бота
bot = Bot(token=BOT_TOKEN)

# Создаем объект диспетчера для обработки сообщений
dp = Dispatcher(bot)


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    Отправляем приветственное сообщение и инлайн-клавиатуру с кнопками
    """
    # Создаем клавиатуру с кнопками
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Подгруппа 1', callback_data='button1')
    button2 = types.InlineKeyboardButton('Подгруппа 2', callback_data='button2')
    keyboard.add(button1, button2)

    # Отправляем приветственное сообщение и инлайн-клавиатуру пользователю
    await message.answer(
        "Привет! Я бот с инлайн-кнопками. Нажми на кнопку, чтобы вызвать действие.",
        reply_markup=keyboard
    )


# Обработчик инлайн-кнопок
@dp.callback_query_handler(lambda c: c.data in ['button1', 'button2'])
async def process_callback_button(callback_query: types.CallbackQuery):
    """
    Обрабатываем нажатие на инлайн-кнопку
    """
    # Получаем название нажатой кнопки
    button = callback_query.data

    # Отправляем сообщение с текстом кнопки
    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=f"Вы нажали на кнопку '{button}'"
    )

    # Отвечаем на запрос пользователя, чтобы убрать уведомление о нажатии на кнопку
    await bot.answer_callback_query(callback_query.id)


# Запускаем бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)




# # Включаем логирование, чтобы отслеживать ошибки
# logging.basicConfig(level=logging.INFO)
#
# # Токен бота можно получить у BotFather в Telegram
#
# # Создаем объект бота
# bot = Bot(token=BOT_TOKEN)
#
# # Создаем объект диспетчера для обработки сообщений
# dp = Dispatcher(bot)
#
#
# # Обработчик команды /start
# @dp.message_handler(commands=['start'])
# async def send_welcome(message: types.Message):
#     """
#     Отправляем приветственное сообщение и клавиатуру с кнопками
#     """
#     # Создаем клавиатуру с кнопками
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     button1 = types.KeyboardButton('1')
#     button0 = types.KeyboardButton('0')
#     keyboard.add(button1, button0)
#
#     # Отправляем приветственное сообщение и клавиатуру пользователю
#     await message.answer(
#         "Привет! Я бот с кнопками. Нажми на кнопку, чтобы выбрать 1 или 0.",
#         reply_markup=keyboard
#     )
#
#
# # Обработчик всех сообщений, кроме команд
# @dp.message_handler()
# async def echo_message(message: types.Message):
#     """
#     Отправляем эхо-ответ на сообщение пользователя
#     """
#     await message.answer(f"Ты выбрал {message.text}")
#
#
# # Запускаем бота
# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)
