import pyexcel as p
import os

fds = sorted(os.listdir('Admin/Downloads/'))

for file in fds:
    if file.endswith('.xls'):
        p.save_book_as(file_name='Admin/Downloads/'+file,
                       dest_file_name='Admin/Downloads/'+file+'.xlsx')
        os.remove('Admin/Downloads/'+file)
