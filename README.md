# LesMehBot - Schedule Parser and Telegram Bot

## Overview

LesMehBot is a project aimed at providing an automated solution for parsing the schedule of Cherepovets Forestry and Mechanical Engineering College (ЧЛМТ) and delivering it to students through a Telegram bot. The project consists of various scripts responsible for downloading, formatting, parsing, and presenting the schedule information.

## Project Structure

- [Download_xls.py](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/Download_xls.py): Downloads xls and xlsx files from the college's website.

- [Reformat_delete.py](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/Reformat_delete.py): Contains functions for renaming and ensuring correct file naming.

- [Search_groups.py](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/Search_groups.py): Contains a function for locating cells containing group names, serving as a reference during parsing.

- [Reader.py](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/Reader.py): The main script responsible for extracting useful information from Excel files and organizing it into a structured JSON format. The functions include error handlers for various Excel file variations.

- [Parser.py](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/Parser.py): Outlines the sequence of methods to be executed by the parser.

- [bot.py](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/bot.py): Contains the complete functionality of the Telegram bot built using aiogram2.

- [requirements.txt](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/requirements.txt): Lists the necessary dependencies for the project.

## Usage

To run the project on your device, replace BOT_TOKEN with the token of your Telegram bot in the [bot.py](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/bot.py) file. Execute the necessary scripts for downloading, formatting, and parsing the schedule.

For Docker:
1. Update the BOT_TOKEN in [bot.py](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/bot.py).
2. Run the bash script that will download dependencies and launch [bot.py](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/bot.py) and [Parser.py](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/Parser.py).

## Contributions

Contributions to enhance or improve the project are welcome. Feel free to submit pull requests or open issues.

## License

This project is licensed under the [MIT License](LICENSE.md). You are free to use and modify the code according to your needs.

---

# LesMehBot - Парсер Расписания и Телеграм-Бот

## Обзор

LesMehBot - это проект, направленный на автоматизацию парсинга расписания Череповецкого Лесо-Механического техникума (ЧЛМТ) и предоставление этой информации студентам через телеграм-бота. Проект состоит из различных скриптов, ответственных за загрузку, форматирование, парсинг и предоставление информации о расписании.

## Структура Проекта

- [Download_xls.py](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/Download_xls.py): Загружает файлы xls и xlsx с веб-сайта колледжа.

- [Reformat_delete.py](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/Reformat_delete.py): Содержит функции для переименования и обеспечения правильного именования файлов.

- [Search_groups.py](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/Search_groups.py): Содержит функцию для поиска ячеек с названиями групп, служащую ориентиром в процессе парсинга.

- [Reader.py](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/Reader.py): Основной скрипт, ответственный за извлечение полезной информации из файлов Excel и организацию ее в структурированный JSON-формат. Функции включают обработчики ошибок для различных вариантов оформления файлов Excel.

- [Parser.py](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/Parser.py): Описывает последовательность методов, которые должны выполняться парсером.

- [bot.py](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/bot.py): Содержит полный функционал телеграм-бота, построенного с использованием aiogram2.

- [requirements.txt](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/requirements.txt): Список необходимых зависимостей для проекта.

## Использование

Для запуска проекта на вашем устройстве замените BOT_TOKEN на токен вашего телеграм-бота в файле [bot.py](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/bot.py). Выполните необходимые скрипты для загрузки, форматирования и парсинга расписания.

Для Docker:
1. Обновите BOT_TOKEN в файле [bot.py](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/bot.py).
2. Запустите bash-скрипт, который загрузит зависимости и запустит [bot.py](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/bot.py) и [Parser.py](https://github.com/xEnotWhyNotx/LesMehBot/blob/master/src/Parser.py).

## Вклад

Приветствуются вклады для улучшения проекта. Не стесняйтесь предлагать pull-запросы или открывать вопросы.

## Лицензия

Этот проект лицензирован в соответствии с [лицензией MIT](LICENSE.md). Вы можете свободно использовать и изменять код в соответствии со своими потребностями.
