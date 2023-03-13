import os
import glob
import re
from datetime import datetime, date, timedelta


def get_filtered_files(group_name, subgroup):
    directory = 'Admin/Destination'
    today = date.today()
    filtered_files = []
    for file_name in os.listdir(directory):
        if group_name in file_name and '__{}__'.format(subgroup) in file_name:
            date_start = file_name.find(' на ') + 4
            if date_start < 4:
                continue
            date_end = file_name.find('.xls', date_start)
            if date_end < 0:
                date_end = file_name.find('___НОВОЕ___.xls', date_start)
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


def find_date_from_name_file(group_name, subgroup):
    files = get_filtered_files(group_name, subgroup)
    date_str = []
    for file in files:
        date_start = file.find(" на ") + 4
        date_end = file.find(".2023")
        date_str.append(file[date_start:date_end])
    return date_str


def reading(group_name, subgroup, date):
    files = get_filtered_files(group_name, subgroup)
    date_for_use = date
    data_dir = 'Admin/Destination/'
    for file in files:
        if file.find(str(date_for_use)) > 0:
            file_for_use = file
            file_path = os.path.join(data_dir, file_for_use)

            with open(file_path, "r") as f:
                content = f.read()

            lines = content.split('\n')

            group_name = lines[0].split(";")[0]
            subject_teacher_names = lines[0].split(";")[1].split(",")
            subject_names = subject_teacher_names[::2]
            teacher_names = subject_teacher_names[1::2]

            classroom_numbers = lines[1].split(";")[1].split(",")
            classroom_numbers = [num.strip() for num in classroom_numbers]

            output = f"Расписание группы {group_name}\n"
            for i in range(len(subject_names)):
                sub_name = subject_names[i].replace("'", "").replace('[', '').replace(']', '')
                tech_name = teacher_names[i].replace('[', '').replace(']', '').replace("'", "")
                class_name = classroom_numbers[i].replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace("'", "")
                if sub_name != 'None':
                    output += f"{i + 1}. {sub_name}\n"
                if tech_name != 'None':
                    output += f"   {tech_name}\n"
                if class_name != 'None':
                    output += f"   Аудитория: {class_name}\n"

            return output
#
# print(reading("ОЛ-11", "1", "09.03"))