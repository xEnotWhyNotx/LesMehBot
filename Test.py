import os
from openpyxl import load_workbook


data_dir = 'Admin/Downloads'
txt_files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
xlsx_files = [v for v in os.listdir(data_dir) if v.endswith('.xlsx')]

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

        data_items = data.items()
        for key, value in data_items:
            cell_group = value
            column_group = str(cell_group)[0]
            row_group = int(str(cell_group)[1:])
            print(row_group)
            #print(key)


# for file in xlsx_files:
# # получаем номер строки и столбца из второй строки коллекции
# row_num, col_num =
#
# # загружаем файл Excel из директории "Admin/Downloads"
# filepath = os.path.join("Admin", "Downloads", filename)
# wb = load_workbook(filepath)
#
# # получаем активный лист
# ws = wb.active
#
# # ищем значения в ячейках ниже на одну или две от известной ячейки
# for row_offset in range(1, 3):
#     for col_offset in range(-1, 2):
#         # пропускаем текущую ячейку
#         if row_offset == 0 and col_offset == 0:
#             continue
#         # получаем значение ячейки
#         cell_value = ws.cell(row=row_num+row_offset, column=col_num+col_offset).value
#         if cell_value:
#             print(cell_value)
