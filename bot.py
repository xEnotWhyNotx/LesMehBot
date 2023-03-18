import logging
import os
import re
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from INFO import BOT_TOKEN
from datetime import datetime, date, timedelta

logging.basicConfig(level=logging.INFO)

# Создаем экземпляр бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

with open('all_data.json') as f:
    data_json = json.load(f)

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

subgroups = ['1', '2']
user_data = {}


async def split_groups(group):
    split_groups = []
    if len(group) > 5:
        prefix, suffixes = group.split('-')
        for suffix in suffixes.split(','):
            split_groups.append(f"{prefix}-{suffix}")
    else:
        split_groups.append(group)
    return split_groups


def search_date(group, subgroup):
    dates = set()
    for date in data_json:
        day_info = data_json[date]
        date_clear = str(date).replace('[', '').replace(']', '').replace("'", "")
        for collect in day_info:
            for key in collect:
                if collect == group and subgroup == '1':
                    dates.add(date_clear)
                if collect == group and subgroup == '2':
                    dates.add(date_clear)
    timeList = list(dates)
    return sorted(timeList)


async def reading_json(group_name, subgroup, date_search):
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


async def search_in_splitted_groups(group_num):
    group_nuzn = ''
    for group in groups:
        groups_splitted = await split_groups(group)
        if group_num in groups_splitted:
            group_nuzn = group
    return group_nuzn


# Обработчик команды /start или текстового сообщения с названием группы
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    # Отправляем сообщение с приветствием и инструкцией
    await message.reply("Привет! Я помогу тебе получить расписание занятий. "
                        "Введите название группы, например 'ОЛ-11' или 'ОЛ-21'.")


# Обработчик сообщений с названием группы
@dp.message_handler(lambda message: message.text.upper() in groups1)
async def process_group_command(message: types.Message):
    # Запоминаем выбранную группу
    user_data['group'] = await search_in_splitted_groups(message.text.upper())

    # Создаем клавиатуру с кнопками подгрупп
    keyboard = InlineKeyboardMarkup()
    for subgroup in subgroups:
        keyboard.add(InlineKeyboardButton(subgroup, callback_data=subgroup))

    # Отправляем сообщение с клавиатурой
    await message.reply("Выбери подгруппу", reply_markup=keyboard)


# Обработчик нажатия на кнопку подгруппы
@dp.callback_query_handler(lambda c: c.data in subgroups)
async def subgroup_callback_handler(callback_query: types.CallbackQuery):
    # Получаем выбранную подгруппу
    subgroup = callback_query.data
    user_data['subgroup'] = subgroup

    # Создаем клавиатуру с кнопками дат
    keyboard = InlineKeyboardMarkup()

    dates = search_date(user_data['group'], user_data['subgroup'])

    for date in dates:
        keyboard.add(InlineKeyboardButton(date, callback_data=date))

    # Отправляем сообщение с клавиатурой
    await bot.send_message(callback_query.from_user.id, f"Вы выбрали {subgroup}. Выберите дату:", reply_markup=keyboard)

    # Отвечаем на callback_query, чтобы скрыть у пользователя кнопки с подгруппами
    await callback_query.answer()


# Обработчик нажатия на кнопку даты
@dp.callback_query_handler(lambda c: c.data in search_date(user_data['group'], user_data['subgroup']))
async def date_callback_handler(callback_query: types.CallbackQuery):
    # Получаем выбранную дату
    date = callback_query.data
    user_data['date'] = date

    # Создаем клавиатуру с кнопкой "назад"
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Назад", callback_data="back"))

    # Отправляем сообщение с клавиатурой
    await bot.send_message(callback_query.from_user.id,
                           f"Выбрана подгруппа {user_data['subgroup']} группы {user_data['group']}",
                           reply_markup=keyboard)

    # Отвечаем на callback_query, чтобы скрыть у пользователя кнопки с датами
    await callback_query.answer()

    # Вызываем функцию reading() и отправляем результат пользователю
    result = await reading_json(user_data['group'], user_data['subgroup'], user_data['date'])
    await bot.send_message(callback_query.from_user.id, result)


# Обработчик нажатия на кнопку "назад"
@dp.callback_query_handler(lambda c: c.data == "back")
async def back_callback_handler(callback_query: types.CallbackQuery):
    # Создаем клавиатуру с кнопками дат
    keyboard = InlineKeyboardMarkup()
    dates = search_date(user_data['group'], user_data['subgroup'])
    for date in dates:
        keyboard.add(InlineKeyboardButton(date, callback_data=date))

    # Отправляем сообщение с клавиатурой
    await bot.send_message(callback_query.from_user.id, "Выберите дату:", reply_markup=keyboard)

    # Отвечаем на callback_query, чтобы скрыть у пользователя кнопку "назад"
    await callback_query.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
