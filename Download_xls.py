import os
import requests
import re
from bs4 import BeautifulSoup

url = 'https://lesmeh.edu35.ru/59-raspisanie-zanyatij'
# Путь для сохранения файла. В папку загрузки
directory = "Admin\Downloads"

fds = sorted(os.listdir('Admin/Downloads/'))
response = requests.get(url)
if response.status_code == (200 or 0):
    for file in fds:
        os.remove('Admin/Downloads/' + file)

if not os.path.exists(directory):
    os.makedirs(directory)

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

for a in soup.find_all('a', href=True):
    if a['href'].endswith('.xls'):
        link = a['href']
        filename = link.split('/')[-1].split(r'(\w+ \d{2}\.\d{2}\.\d{2}.')[0]
        filepath = os.path.join(directory, filename)
        response = requests.get(link)
        with open(filepath, 'wb') as f:
            f.write(response.content)
            print(f'{filename} скачан')

print('Загрузка завершена')
