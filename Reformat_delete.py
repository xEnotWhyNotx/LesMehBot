import pyexcel as p
import os


def Reformat_and_delete():
    fds = sorted(os.listdir('Admin/Downloads/'))

    for file in fds:
        if file.endswith('.xls'):
            p.save_book_as(file_name='Admin/Downloads/'+file,
                           dest_file_name='Admin/Downloads/'+file+'.xlsx')
            os.remove('Admin/Downloads/'+file)

def add_new_to_file_name():
    directory = "Admin/Destination/"
    fds = sorted(os.listdir('Admin/Destination/'))

    for file_name in fds:
        file_path = directory + file_name
        date_start = file_name.find(' на ') + 4
        # if date_start < 4:
            # return file_name
        date_end = file_name.find('2023', date_start)
        date_end = date_end + 4
        file_name_end = file_name.find('.xls', date_end)
        if file_name == date_end:
            # return file_name
            continue
        if abs(date_end - file_name_end) > 0:
            new_name = file_name[:date_end] + '___НОВОЕ___' + file_name[file_name_end:]
            new_file_path = directory + new_name
            os.rename(file_path, new_file_path)
        #     return new_name
        # return file_name
