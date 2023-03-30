import logging
import json
import time
import aioschedule
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from aiogram.utils import executor
from datetime import datetime, date, timedelta
from INFO import BOT_TOKEN, ADMIN_PASSWORD, ADMINS

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
admins = set()

# создаем логгер
bot_logger = logging.getLogger('bot_logger')
# создаем обработчик логов, который будет записывать сообщения в файл
bot_handler = logging.FileHandler('bot.log')
# создаем форматировщик сообщений, чтобы добавлять дату и время выполнения запроса
bot_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# привязываем обработчик к логгеру и добавляем к нему форматировщик сообщений
bot_handler.setFormatter(bot_formatter)
bot_logger.addHandler(bot_handler)
# устанавливаем уровень логирования, чтобы сохранять только сообщения с уровнем INFO и выше
bot_logger.setLevel(logging.INFO)

# создаем логгер
user_logger = logging.getLogger('user_logger')
# создаем обработчик логов, который будет записывать сообщения в файл
user_handler = logging.FileHandler('users.log')
# создаем форматировщик сообщений, чтобы добавлять дату и время выполнения запроса
user_formatter = logging.Formatter('%(asctime)s - %(message)s')
# привязываем обработчик к логгеру и добавляем к нему форматировщик сообщений
user_handler.setFormatter(user_formatter)
user_logger.addHandler(user_handler)
# устанавливаем уровень логирования, чтобы сохранять только сообщения с уровнем INFO и выше
user_logger.setLevel(logging.INFO)

# создаем логгер
chat_logger = logging.getLogger('chat_logger')
# создаем обработчик логов, который будет записывать сообщения в файл
chat_handler = logging.FileHandler('chat.log')
# создаем форматировщик сообщений, чтобы добавлять дату и время выполнения запроса
chat_formatter = logging.Formatter('%(asctime)s - %(message)s')
# привязываем обработчик к логгеру и добавляем к нему форматировщик сообщений
chat_handler.setFormatter(chat_formatter)
chat_logger.addHandler(chat_handler)
# устанавливаем уровень логирования, чтобы сохранять только сообщения с уровнем INFO и выше
chat_logger.setLevel(logging.INFO)


# Определение класса состояний FSM
class AdminState(StatesGroup):
    menu = State()
    admin_login = State()


class UserState(StatesGroup):
    WAITING_ADMIN_LOGIN = State()
    WAITING_ADMIN_PASSWORD = State()
    UPDATING = State()
    WAITING_GROUP_NAME = State()
    WAITING_SUBGROUP = State()
    WAITING_DATE = State()


# Список групп
groups = ['АМ-31,33', 'АМ-32,34', 'АМ-41', 'АМ-42,43', 'АС-11', 'АЭ-11', 'АЭ-21,22', 'АЭ-31,32', 'БУ-21,22',
          'БУ-31,32', 'ИС-11', 'ИС-12', 'ИС-13', 'ИС-21,23', 'ИС-22,24', 'ИС-31,34',
          'ИС-32,35', 'ИС-33,36', 'ИС-41,43', 'ИС-42,44', 'ЛЗ-11', 'ЛЗ-21,22', 'ЛЗ-31,32', 'ЛЗ-41', 'ЛП-11',
          'МЭ-11', 'МЭ-21,22', 'МЭ-31,32', 'МЭ-41,42', 'ОЛ-11', 'ОЛ-21,22', 'ОЛ-31,32',
          'ОП-11', 'ОП-21,22', 'ОП-31,32', 'ОП-41,44', 'РД-11', 'РЗ-11', 'ТД-11', 'ТД-21,22', 'ТД-31,32',
          'ТД-41,42', 'ТП-11', 'ТП-21', 'ТП-31,32', 'ТП-41', 'ЭМ-11', 'ЭМ-12', 'ЭМ-21,22',
          'ЭМ-31,32', 'ЭМ-41,43', 'ЭМ-42,44', 'ЭС-11', 'ЭС-21', 'ЭС-31,32', 'ЭС-41,42', 'ЮР-11,13', 'ЮР-12',
          'ЮР-21,23', 'ЮР-22,24', 'ЮР-25', 'ЮР-31,33', 'ЮР-32,34', 'ЮР-35,36']

groups1 = ['АМ-31', 'АМ-33', 'АМ-32', 'АМ-34', 'АМ-41', 'АМ-42', 'АМ-43', 'АС-11', 'АЭ-11', 'АЭ-21', 'АЭ-22', 'АЭ-31',
           'АЭ-32', 'БУ-21', 'БУ-22', 'БУ-31', 'БУ-32', 'ИС-11', 'ИС-12', 'ИС-13', 'ИС-21', 'ИС-23', 'ИС-22', 'ИС-24',
           'ИС-31', 'ИС-34',
           'ИС-32', 'ИС-35', 'ИС-33', 'ИС-36', 'ИС-41', 'ИС-43', 'ИС-42', 'ИС-44', 'ЛЗ-11', 'ЛЗ-21', 'ЛЗ-22', 'ЛЗ-31',
           'ЛЗ-32', 'ЛЗ-41', 'ЛП-11', 'МЭ-11', 'МЭ-21', 'МЭ-22', 'МЭ-31', 'МЭ-32', 'МЭ-41', 'МЭ-42', 'ОЛ-11', 'ОЛ-21',
           'ОЛ-22', 'ОЛ-31', 'ОЛ-32',
           'ОП-11', 'ОП-21', 'ОП-22', 'ОП-31', 'ОП-32', 'ОП-41', 'ОП-44', 'РД-11', 'РЗ-11', 'ТД-11', 'ТД-21', 'ТД-22',
           'ТД-31', 'ТД-32', 'ТД-41', 'ТД-42', 'ТП-11', 'ТП-21', 'ТП-31', 'ТП-32', 'ТП-41', 'ЭМ-11', 'ЭМ-12', 'ЭМ-21',
           'ЭМ-22',
           'ЭМ-31', 'ЭМ-32', 'ЭМ-41', 'ЭМ-43', 'ЭМ-42', 'ЭМ-44', 'ЭС-11', 'ЭС-21', 'ЭС-31', 'ЭС-32', 'ЭС-41', 'ЭС-42',
           'ЮР-11', 'ЮР-13', 'ЮР-12', 'ЮР-21', 'ЮР-23', 'ЮР-22', 'ЮР-24', 'ЮР-25', 'ЮР-31', 'ЮР-33', 'ЮР-32', 'ЮР-34',
           'ЮР-35', 'ЮР-36']

SUBGROUPS = ['1', '2']


async def search_in_splitted_groups(group_num):
    group_nuzn = ''
    for group in groups:
        groups_splitted = await split_groups(group)
        if group_num in groups_splitted:
            group_nuzn = group
    return group_nuzn


async def split_groups(group):
    split_groups = []
    if len(group) > 5:
        prefix, suffixes = group.split('-')
        for suffix in suffixes.split(','):
            split_groups.append(f"{prefix}-{suffix}")
    else:
        split_groups.append(group)
    return split_groups


async def search_date(group, subgroup):
    try:
        today = date.today()
        with open('all_data.json') as f:
            data_json = json.load(f)
        dates = set()
        for day in data_json:
            day_info = data_json[day]
            date_clear = str(day).replace('[', '').replace(']', '').replace("'", "")
            date_for = date_clear + '.2023'
            for collect in day_info:
                if collect == group and subgroup == '1':
                    file_date = datetime.strptime(date_for, '%d.%m.%Y').date()
                    if file_date >= today:
                        dates.add(date_clear)
                if collect == group and subgroup == '2':
                    file_date = datetime.strptime(date_for, '%d.%m.%Y').date()
                    if file_date >= today:
                        dates.add(date_clear)
        timeList = list(dates)
        return sorted(timeList)
    except Exception:
        time.sleep(5)
        await search_date(group, subgroup)


async def reading_json(group_name, subgroup, date_search):
    try:
        with open('all_data.json') as x:
            data_json = json.load(x)
    except Exception:
        time.sleep(5)
        with open('all_data.json') as x:
            data_json = json.load(x)

    key_day = date_search
    key_group = group_name
    key_subgroup = subgroup

    lessons = data_json[key_day][key_group][key_subgroup]['lesson']
    teachers = data_json[key_day][key_group][key_subgroup]['teacher']
    auds = data_json[key_day][key_group][key_subgroup]['aud']

    output = f"Расписание группы {group_name}\n"
    for i in range(len(lessons)):
        sub_name = lessons[i]
        tech_name = teachers[i]
        class_name = auds[i]
        if sub_name != 'None':
            output += f"{i + 1}. {sub_name}\n"
        if tech_name != 'None':
            output += f"    {tech_name}\n"
        if class_name != 'None':
            output += f"    Аудитория: {class_name}\n"
    return output


# Функция для добавления пользователя в список администраторов
async def add_admin(user_id: int):
    """
    Функция для добавления пользователя в список администраторов
    """
    # Добавляем user_id в список администраторов
    admins.add(user_id)


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    """
    Обработчик команды /start
    """
    # сохраняем информацию о запросе в лог-файле
    bot_logger.info(f"User {message.from_user.id, message.from_user.username} started the bot")
    user_logger.info(f"{message.from_user.id, message.from_user.username}")
    await message.answer(
        "Привет!\n"
        "Help-меню вызывается командой /help\n"
        "Напиши номер группы\n"
        "(например ОЛ-11):🔍")
    # await cmd_help(message)


# Обработчик команды /help
@dp.message_handler(Command("help"))
async def cmd_help(message: types.Message):
    """
    Обработчик команды /help
    """
    # сохраняем информацию о запросе в лог-файле
    bot_logger.info(f"User {message.from_user.id, message.from_user.username} entered to help menu")
    await message.answer(
        "Вот список моих команд:👨‍💻\n"
        "/start - начать работу 👾\n"
        "/help - получить список команд 🆘\n"
        "/back - вернуться к выбору групп 🔍\n"
        "/admin - админка 😎\n"
        "Повторно прописывать команду /start не требуется, ты можешь сразу писать нужную группу :)\n"
        "\n\nИ да, бота можно использовать в беседах. Не забудь, при добавлении бота в чат, выдать ему администратора, иначе он не сможет ответить на твои сообщения"
    )


# Обработчик команды /admin
@dp.message_handler(Command("admin"))
# Функция для входа в админку
async def admin_login(message: types.Message):
    """
    Функция для входа в админку
    """
    # сохраняем информацию о запросе в лог-файле
    bot_logger.info(f"User {message.from_user.id, message.from_user.username} entered to admin login menu")
    await message.answer('Введите пароль для входа в админ-панель:')
    # Переводим бота в состояние ожидания пароля для входа в админ-панель
    await AdminState.admin_login.set()


# Обработка пароля для входа в админку
@dp.message_handler(state=AdminState.admin_login)
async def process_admin_login(message: types.Message, state: FSMContext):
    """
    Обработка пароля для входа в админку
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Stats", callback_data="admin_stats"),
        InlineKeyboardButton("Logs", callback_data="admin_log_upload"),
        InlineKeyboardButton("Users", callback_data="admin_user_upload"),
        InlineKeyboardButton("Chats", callback_data="admin_chat_upload"),
        InlineKeyboardButton("Exit", callback_data="admin_exit"),
    )
    # Проверяем, является ли введенный пароль правильным
    if message.text == ADMIN_PASSWORD:
        # Удаляем состояние admin_login из контекста состояний
        await state.finish()
        # Добавляем пользователя в список администраторов
        await add_admin(message.from_user.id)
        # Отправляем сообщение об успешном входе в админ-панель
        await message.answer(str(admins))
        await message.answer('Добро пожаловать в админ-панель!', reply_markup=keyboard)
        # сохраняем информацию о запросе в лог-файле
        bot_logger.info(f"User {message.from_user.id, message.from_user.username} entered to admin panel")
        await AdminState.menu.set()
    elif message.text == '0':
        await message.answer('Вы вышли из режима авторизации\n'
                             'Напиши номер группы или используй команду /help')
        await state.reset_state()
    else:
        # Отправляем сообщение об ошибке в случае неправильного пароля
        await message.answer('Неверный пароль для входа в админ-панель!\n'
                             'Чтобы выйти из режима авторизации напиши "0"')
        # сохраняем информацию о запросе в лог-файле
        bot_logger.info(f"User {message.from_user.id, message.from_user.username} entered invalid password")


# Обработчик инлайн-кнопок админ-панели
@dp.callback_query_handler(state=AdminState.menu)
async def process_callback_admin(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обработчик инлайн-кнопок админ-панели
    """
    data = callback_query.data
    if data == "admin_stats":
        await bot.answer_callback_query(callback_query.id, text="Текущая статистика: ...")
    elif data == "admin_log_upload":
        with open('bot.log', 'rb') as file:
            # отправляем файл ботом
            await bot.send_document(callback_query.from_user.id, file)
            file.close()
        # удаляем все данные из файла
        with open("bot.log", "w") as file:
            file.write("")
            file.close()
    elif data == "admin_chat_upload":
        with open('chat.log', 'rb') as file:
            # отправляем файл ботом
            await bot.send_document(callback_query.from_user.id, file)
            file.close()
        # удаляем все данные из файла
        with open("chat.log", "w") as file:
            file.write("")
            file.close()
    elif data == "admin_user_upload":
        with open('users.log', 'rb') as file:
            # отправляем файл ботом
            await bot.send_document(callback_query.from_user.id, file)
    elif data == "admin_exit":
        await bot.answer_callback_query(callback_query.id, text="Вы вышли из админ-панели.")
        await state.finish()


@dp.message_handler(lambda message: message.text.upper() not in groups1)
async def process_invalid_group_name(message: types.Message):
    user_logger.info(f"{message.from_user.id, message.from_user.username}")
    # сохраняем информацию о запросе в лог-файле
    chat_logger.info(
        f"chat {message.chat.id, message.chat.title} user {message.from_user.id, message.from_user.username} text {message.text}")


@dp.message_handler(lambda message: message.text.upper() in groups1)
async def process_group_name(message: types.Message, state: FSMContext):
    await UserState.WAITING_GROUP_NAME.set()
    group_name = await search_in_splitted_groups(message.text.upper())
    user_logger.info(f"{message.from_user.id, message.from_user.username}")
    # сохраняем информацию о запросе в лог-файле
    bot_logger.info(
        f"User {message.from_user.id, message.from_user.username} selected {message.text.upper(), group_name}")
    keyboard = InlineKeyboardMarkup(row_width=2)
    for subgroup in SUBGROUPS:
        button = InlineKeyboardButton(
            text=f"Подгруппа {subgroup}",
            callback_data=subgroup
        )
        keyboard.add(button)

    await message.answer(
        "Выберите подгруппу:",
        reply_markup=keyboard,
    )

    await UserState.WAITING_SUBGROUP.set()
    await state.update_data(group_name=group_name)


@dp.callback_query_handler(lambda c: True, state=UserState.WAITING_SUBGROUP)
async def process_subgroup(callback_query: types.CallbackQuery, state: FSMContext):
    subgroup = callback_query.data

    data = await state.get_data()
    group_name = data.get("group_name")

    keyboard = InlineKeyboardMarkup(row_width=2)

    DATES = await search_date(group_name, subgroup)
    print(DATES)
    for date in DATES:
        button = InlineKeyboardButton(
            text=date,
            callback_data=f"{group_name}_{subgroup}_{date}"
        )
        keyboard.add(button)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Выберите день:",
        reply_markup=keyboard,
    )

    await UserState.WAITING_DATE.set()


@dp.callback_query_handler(lambda c: True, state=UserState.WAITING_DATE)
async def process_date(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data.split("_")
    group_name, subgroup, date = data[0], data[1], data[2]

    await bot.answer_callback_query(callback_query.id)

    result_message = await reading_json(group_name, subgroup, date)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=result_message,
        parse_mode=ParseMode.HTML,
    )
    await UserState.WAITING_GROUP_NAME.set()
    await state.finish()


@dp.message_handler(Command("back"), state=UserState.WAITING_SUBGROUP)
@dp.message_handler(Command("back"), state=UserState.WAITING_DATE)
@dp.message_handler(Command("back"), state=AdminState.menu)
@dp.message_handler(Command("back"), state=AdminState.admin_login)
async def cmd_back(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название группы (ОЛ-11 или ОЛ-12):",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.reset_state()


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception:
        time.sleep(5)
        executor.start_polling(dp, skip_updates=True)
