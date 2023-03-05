import os
import requests
import re
from bs4 import BeautifulSoup

url = 'https://lesmeh.edu35.ru/59-raspisanie-zanyatij'
# Путь для сохранения файла. В папку загрузки
directory = "Admin\Downloads"

fds = sorted(os.listdir('Admin/Downloads/'))
for file in fds:
    os.remove('Admin/Downloads/'+file)

if not os.path.exists(directory):
    os.makedirs(directory)

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

for a in soup.find_all('a', href=True):
    if a['href'].endswith('.xls'):
        link = a['href']
        #filename = link.split('/')[-1].split('.')[0].replace('_', '.')
        filename = link.split('/')[-1].split(r'(\w+ \d{2}\.\d{2}\.\d{2}.')[0]
        filepath = os.path.join(directory, filename + '.xls')
        response = requests.get(link)
        with open(filepath, 'wb') as f:
            f.write(response.content)
            print(f'{filename}.xls скачан')

# for a in soup.find_all('a', href=True):
#     if a['href'].endswith('.xls'):
#         link = a['href']
#         filename = re.split(r'[\\/:*?"<>|.\s]+', link)[-1].split('.')[0].replace('(', '').replace(')', '').replace('_', ' ').strip()
#         filepath = os.path.join(directory, filename + '.xls')
#         response = requests.get(link)
#         with open(filepath, 'wb') as f:
#             f.write(response.content)
#             print(f'{filename}.xls скачан')

print('Загрузка завершена')
