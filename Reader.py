import os
import re
import numpy as np
import openpyxl as ox
from openpyxl.utils import get_column_letter

# import pyexcel as p
# from openpyxl import load_workbook


directory = 'Admin/Downloads'
search_text = 'ОЛ-11'
print('Ищем: ', search_text)

for filename in os.listdir(directory):
    if filename.endswith('.xlsx'):
        filepath = os.path.join(directory, filename)
        wb = ox.load_workbook(filename=filepath, read_only=True)
        ws = wb[wb.sheetnames[0]]  # первый лист
        row_max = ws.max_row
        column_max = ws.max_column
        print('In file: ', filename, '\n Columns:', column_max, '\n Rows: ', row_max)
        row_min = 1
        column_min = 1

        arr_A = []
        arr_indexes_A = []
        arr_indexes_without_A = []
        for i in range(row_max + 1):
            word_cell_A = 'A' + str(int(i))
            word_cell_without_A = int(i)
            arr_indexes_A.append(word_cell_A)
            arr_indexes_without_A.append(word_cell_without_A)
            # print(word_cell_A)
            data_from_cell_A = ws[word_cell_A].value
            arr_A.append(data_from_cell_A)

        NoneType = type(None)
        index_to_remove = []
        for j in range(len(arr_A)):
            if type(arr_A[j]) == NoneType:
                index_to_remove.append(j)

        arr_A = np.delete(arr_A, index_to_remove)
        arr_indexes_A = np.delete(arr_indexes_A, index_to_remove)
        arr_indexes_without_A = np.delete(arr_indexes_without_A, index_to_remove)

        # Очистим массивы индексов и данных из ячеек от мусора
        next_clean_arr = []
        for i in range(len(arr_A)):
            nums = '123456'
            if arr_A[i] not in nums:
                next_clean_arr.append(i)
        arr_A = np.delete(arr_A, next_clean_arr)
        arr_indexes_A = np.delete(arr_indexes_A, next_clean_arr)
        arr_indexes_without_A = np.delete(arr_indexes_without_A, next_clean_arr)

        # Функция создания массивов индексов и данных из ячеек
        arr_test = arr_A
        arr_test_ind = arr_indexes_A
        arr_test_ind_without_A = arr_indexes_without_A

        result_arr = []
        result_arr_ind = []
        result_arr_ind_without_A = []

        temp = [arr_test[0]]
        temp_ind = [arr_test_ind[0]]
        temp_ind_without_A = [arr_test_ind_without_A[0]]

        for i in range(1, len(arr_test)):
            if arr_test[i] < arr_test[i - 1]:
                result_arr.append(temp)
                result_arr_ind.append(temp_ind)
                result_arr_ind_without_A.append(temp_ind_without_A)
                temp = []
                temp_ind = []
                temp_ind_without_A = []
            temp.append(arr_test[i])
            temp_ind.append(arr_test_ind[i])
            temp_ind_without_A.append(arr_test_ind_without_A[i])
        result_arr.append(temp)
        result_arr_ind.append(temp_ind)
        result_arr_ind_without_A.append(temp_ind_without_A)

        while column_min <= column_max:
            row_min_min = row_min
            row_max_max = row_max
            while row_min_min <= row_max_max:
                row_min_min = str(row_min_min)

                word_column = get_column_letter(column_min)
                word_column = str(word_column)
                word_cell = word_column + row_min_min

                data_from_lesson = {}
                data_from_teacher = {}
                for i in range(1, 7):
                    lesson_cell = word_column + str(int(row_min_min) + 2 * i - 1)
                    #print(lesson_cell)
                    teacher_cell = word_column + str(int(row_min_min) + 2 * i)
                    #print(teacher_cell)
                    data_from_lesson[f"data_from_lesson_{i}"] = ws[lesson_cell].value
                    data_from_teacher[f"data_from_teacher_{i}"] = ws[teacher_cell].value

                data_from_cell = ws[word_cell].value
                data_from_cell = str(data_from_cell)
                # print(data_from_cell)
                regular = search_text
                result = re.findall(regular, data_from_cell)

                if len(result) > 0:
                    print('Нашли в ячейке: ', word_cell)
                    # data_from_cell_next = ws[word_cell_next].value
                    # print(data_from_cell_next)
                    # print(arr_A)
                    # print(arr_indexes_A)
                    print(result_arr)
                    print(result_arr_ind)
                    print(result_arr_ind_without_A)
                    print(data_from_lesson)
                    print(data_from_teacher)

                row_min_min = int(row_min_min)
                row_min_min += 1
            column_min += 1
