import os
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def Download_xls():
    url = 'https://lesmeh.edu35.ru/59-raspisanie-zanyatij'
    # Путь для сохранения файла. В папку загрузки
    directory = "Admin/Downloads"

    fds = sorted(os.listdir('Admin/Downloads/'))
    response = requests.get(url, timeout=100)
    # if response.status_code == (200 or 0):
    #     for file in fds:
    #         os.remove('Admin/Downloads/' + file)

    if not os.path.exists(directory):
        os.makedirs(directory)

    response = requests.get(url, timeout=100)
    soup = BeautifulSoup(response.text, 'html.parser')

    for a in soup.find_all('a', href=True):
        if a['href'].endswith('.xlsx'):
            link = a['href']
            filename = link.split('/')[-1].split(r'(\w+ \d{2}\.\d{2}\.')[0]
            filepath = os.path.join(directory, filename)
            response = requests.get(link, timeout=100)
            for file in directory:
                if file.endswith(".xlsx") or file.endswith(".txt"):
                    if response.status_code == (200 or 0):
                        os.remove('Admin/Downloads/' + file)

            with open(filepath, 'wb') as f:
                f.write(response.content)
                print(f'{filename} скачан')

    print('Загрузка завершена')


def delete_downloaded_files():
    # Определяем дату, которая является границей для удаления файлов
    border_date = datetime.today() - timedelta(days=2)
    date_pattern =r'\d{2}\.\d{2}'

    # Перебираем все файлы в директории Admin/Downloads
    for filename in os.listdir("Admin/Downloads/"):
        # Проверяем, что файл является файлом расписания
        if filename.startswith("Расписание на "):
            # Получаем дату из названия файла
            match = re.search(date_pattern, filename)
            found_date = str(match.group(0))
            current_year = str(datetime.now().year)
            full_found_date = datetime.strptime(found_date + "." + current_year, "%d.%m.%Y")
            if match and full_found_date <= border_date:
                # Удаляем файл
                os.remove(os.path.join("Admin/Downloads/", filename))
            else:
                continue
