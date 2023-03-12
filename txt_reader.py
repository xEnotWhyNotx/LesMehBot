import os
import glob
import re
from datetime import datetime, date, timedelta


def get_filtered_files(group_name, subgroup):
    directory = 'Admin/Destination'
    # today = date.today()
    today = date.today() - timedelta(days=4)
    filtered_files = []
    for file_name in os.listdir(directory):
        if group_name in file_name and '__{}__'.format(subgroup) in file_name:
            date_start = file_name.find(' на ') + 4
            if date_start < 4:
                continue
            date_end = file_name.find('.xls', date_start)
            if date_end < 0:
                date_end = file_name.find(' .xls', date_start)
                if date_end < 0:
                    continue
            date_str = file_name[date_start:date_end]
            if len(date_str) > 10:
                date_str = date_str[:10]
            try:
                file_date = datetime.strptime(date_str, '%d.%m.%Y').date()
            except ValueError:
                try:
                    file_date = datetime.strptime(date_str, '%d.%m.%y').date()
                except ValueError:
                    continue
            if file_date >= today:
                filtered_files.append(file_name)
    return filtered_files


def find_files_by_subgroup(group_name, subgroup):
    directory = "Admin/Destination/"
    pattern = f"*{group_name}*__{subgroup}__*"
    files = glob.glob(directory + pattern)
    return files


def reading(group_name, subgroup):
    files = get_filtered_files(group_name, subgroup)
    if len(files) > 0:
        print("Найденные файлы:")
        for file_path in files:
            print(file_path)
    else:
        print("Файлы не найдены")

    data_dir = 'Admin/Destination/'
    # txt_files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
    file = 'Расписание на 01.03.2023 .xls_ОЛ-11__1__.txt'
    file_path = os.path.join(data_dir, file)

    with open(file_path, "r") as f:
        content = f.read()

    lines = content.split('\n')

    group_name = lines[0].split(":")[0]
    subject_teacher_names = lines[0].split(":")[2].split(",")
    subject_names = subject_teacher_names[::2]
    teacher_names = subject_teacher_names[1::2]

    classroom_numbers = lines[1].split(":")[1].split(",")
    classroom_numbers = [num.strip() for num in classroom_numbers]

    output = f"Расписание группы {group_name}\n"
    for i in range(len(subject_names)):
        output += f"{i + 1}. {subject_names[i].replace('[', '').replace(']', '')}\n"
        output += f"   {teacher_names[i].replace('[', '').replace(']', '')}\n"
        output += f"   Аудитория: {classroom_numbers[i].replace('{', '').replace('}', '').replace('[', '').replace(']', '')}\n"

    return output


# reading("ОЛ-11", "1")
add_new_to_file_name()
