import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Включаем логирование, чтобы отслеживать ошибки
logging.basicConfig(level=logging.INFO)

# Токен бота можно получить у BotFather в Telegram
BOT_TOKEN = 'токен_бота'

# Создаем объект бота
bot = Bot(token=BOT_TOKEN)

# Создаем объект диспетчера для обработки сообщений
dp = Dispatcher(bot)


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    Отправляем приветственное сообщение и инструкции
    """
    await message.answer(
        "Привет! Я эхо-бот. Я буду отправлять тебе все сообщения, которые ты мне отправишь.\n"
        "Чтобы начать, просто напиши мне что-нибудь."
    )


# Обработчик всех сообщений, кроме команд
@dp.message_handler()
async def echo_message(message: types.Message):
    """
    Отправляем эхо-ответ на сообщение пользователя
    """
    await message.answer(f"Ты написал: {message.text}")


# Запускаем бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
