import os
import openpyxl as ox
from openpyxl import load_workbook


data_dir = 'Admin/Downloads'
txt_files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
xlsx_files = [v for v in os.listdir(data_dir) if v.endswith('.xlsx')]
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for file in txt_files:
    data = {}
    with open(os.path.join(data_dir, file), 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split(': ')
            data[line[0]] = line[1]
    print(file)
    print(data)
    print("__________________________________")

    for filename in xlsx_files:
        if filename.endswith('.xlsx') and (str(filename)[:-4] + "txt") == file:
            #print(filename)
            filepath = os.path.join(data_dir, filename)
            wb = ox.load_workbook(filename=filepath, read_only=True)
            ws = wb[wb.sheetnames[0]]
            row_max = ws.max_row
            column_max = ws.max_column
            print('In file: ', filename, '\n Columns:', column_max, '\n Rows: ', row_max)
            row_min = 1
            column_min = 1

            data_items = data.items()
            for key, value in data_items:
                cell_group = value
                column_group = str(cell_group)[0]
                row_group = int(str(cell_group)[1:])
                # print(row_group)
                # print(key)

                # ищем значения в ячейках ниже на одну или две от известной ячейки
                for row_offset in range(1, 3):
                    for col_offset in range(-1, 2):
                        # пропускаем текущую ячейку
                        if row_offset == 0 and col_offset == 0:
                            continue
                        # получаем значение ячейки
                        cell_value = ws.cell(row=row_group + row_offset, column=alphabet.find(column_group) + col_offset).value
                        if cell_value:
                            print(cell_value)
