import time
from Download_xls import Download_xls
from Reformat_delete import Reformat_and_delete
from Search_groups import Search_groups
from Reader import Reader_files


if __name__ == '__main__':
    start_all_parse = time.time()
    Download_xls()
    Reformat_and_delete()
    Search_groups()
    Reader_files()
    end_all_parse = time.time()
    print("Время полного выполнения программы: ", end_all_parse - start_all_parse, "s")
    print("Время полного выполнения программы: ", (end_all_parse - start_all_parse)/60, "m")
