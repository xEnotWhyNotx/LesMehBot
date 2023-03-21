import time
from Download_xls import Download_xls
from Reformat_delete import Reformat_and_delete, add_new_to_file_name, delete_files
from Search_groups import Search_groups
from Reader import Reader_files


def parser():
    try:
        start_all_parse = time.time()
        Download_xls()
        Reformat_and_delete()
        Search_groups()
        Reader_files()
        add_new_to_file_name()
        delete_files()
        end_all_parse = time.time()
        print("Время полного выполнения программы: ", end_all_parse - start_all_parse, "s")
        print("Время полного выполнения программы: ", (end_all_parse - start_all_parse) / 60, "m")
    except ConnectionError or Exception:
        print("connection_problem")
        parser()


if __name__ == '__main__':
    while True:
        parser()
        time.sleep(120)

