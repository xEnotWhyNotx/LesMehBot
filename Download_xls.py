import os
import requests
from bs4 import BeautifulSoup

url = 'https://lesmeh.edu35.ru/59-raspisanie-zanyatij'
# Путь для сохранения файла. В папку загрузки
directory = "Admin\Downloads"

if not os.path.exists(directory):
    os.makedirs(directory)

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

for a in soup.find_all('a', href=True):
    if a['href'].endswith('.xls'):
        link = a['href']
        filename = link.split('/')[-1].split('.')[0].replace('_', '.')
        filepath = os.path.join(directory, filename + '.xls')
        response = requests.get(link)
        with open(filepath, 'wb') as f:
            f.write(response.content)
            print(f'{filename}.xls скачан')

print('Загрузка завершена')
