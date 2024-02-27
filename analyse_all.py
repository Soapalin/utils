from Logger import log
import sys
import os
from enum import Enum 



TRUNK = r"C:\Sandbox\gen5_0"
os.system(f"svn update {TRUNK}")


class TC_RESULT(Enum):
    NOT_EX = 0
    PASS = 1
    FAIL = 2



def analyse_file(path):
    global RESULT
    # print("\n")
    # log.debug(path)

    if not path.endswith(".log"):
        log.debug(f"{path} is not a log file.")
        return
    
    with open(path) as f:
        data = f.readlines()


    file_path = ""
    if "/" in path:
        file_path = path.split("/")[-1]
    if "\\" in path:
        file_path = path.split("\\")[-1]


        if len(data) == 0:
            log.not_ex(f"{file_path} not executed")
            return TC_RESULT.NOT_EX
        for line in data:
            if "ms F" in line:
                log.failed(f"{file_path} failed")
                return TC_RESULT.FAIL
            
        log.passed(f"{file_path} passed")
        return TC_RESULT.PASS

def analyse_folder(log_folder, result_sheet):
    global RESULT
    log.info(f"Folder: {log_folder}")

    RESULT = f"RESULT_{result_sheet}.csv"
    log.info(RESULT)

    if os.path.isdir(log_folder):
        onlyfiles = [f for f in os.listdir(log_folder) if os.path.isfile(os.path.join(log_folder, f))]
        with open(RESULT, "w") as w:
            for file in onlyfiles:
                if "_full.log" in file:
                    res = analyse_file(os.path.join(log_folder, file))
                    if res == TC_RESULT.FAIL:
                        w.write(f"{file}, FAIL\n")
                    elif res == TC_RESULT.NOT_EX:
                        w.write(f"{file}, NOT_EX\n")
                    elif res == TC_RESULT.PASS:
                        w.write(f"{file}, PASS\n")
        if os.stat(RESULT).st_size == 0:
            os.remove(RESULT)


        onlyfolder = [f for f in os.listdir(log_folder) if os.path.isdir(os.path.join(log_folder, f))]
        for fold in onlyfolder:
            analyse_folder(os.path.join(log_folder, fold),f"{result_sheet}_{fold}")


def usage():
    print("To run this script: $ python analyse_all.py [log_folder]")

if len(sys.argv) > 1: 
    log.info(f"Folder: {sys.argv[1]}")
    log_folder = sys.argv[1]

    if not os.path.exists(log_folder):
        log.error(f"{log_folder} does not exist.")
        sys.exit()

    if os.path.isfile(log_folder):
        log.info(f"{log_folder} is a file.")
        analyse_file(log_folder)
        sys.exit()

    file_path = ""
    if "/" in log_folder:
        file_path = log_folder.split("/")[-1]
    if "\\" in log_folder:
        file_path = log_folder.split("\\")[-1]
    
    RESULT = f"{file_path}"

    analyse_folder(log_folder,RESULT)


    # if os.path.isdir(log_folder):
    #     onlyfiles = [f for f in os.listdir(log_folder) if os.path.isfile(os.path.join(log_folder, f))]
    #     log.debug(onlyfiles)
    #     for file in onlyfiles:
    #         if "_full.log" in file:
    #             analyse_file(os.path.join(log_folder, file))

else:
    usage()



