import numpy as np
import os
import sqlite3 as sql
import glob
# file1 = open(os.path.expanduser('8-08-17/noTime_yesCC_ironPipeFail.txt'), 'r')
# list1 = file1.read().splitlines()
filepath = input("Where is the directory with the output?\n")
files = glob.glob(filepath + "/*.db")
# print(files_)
# files = [x for x in files_ if x.split('/')[1].split('.')[0] == 'db']
print(files)
run_time = 150
for Path in files:
    db = sql.connect(Path)
    com = db.cursor()

    yearList = list()
    breakCountpvc = list()
    breakCountiron = list()
    breakCountpump = list()
    db_table_list = ["failureData"]
    break_count_by_simulation_list = list()
    for simulation_index, simulation in enumerate(db_table_list):
        count = 0
        break_count_by_simulation_list.append([list(), list(), list()])
        while count < run_time:
            break_count_by_simulation_list[simulation_index][0].append(0)
            break_count_by_simulation_list[simulation_index][1].append(0)
            break_count_by_simulation_list[simulation_index][2].append(0)
            count += 1

    count = 0
    while count < run_time:
        yearList.append(count)
        count += 1

    for simulation_index, simulation in enumerate(db_table_list):
        for item in com.execute(('SELECT * FROM {} ORDER BY Bihour_Count ASC').format(simulation)):
            thisIndex = int(np.floor((int(item[0]) / 4380)))
            if item[2] == "pump":
                break_count_by_simulation_list[simulation_index][0][thisIndex] += 1
            if item[2] == "pvc":
                break_count_by_simulation_list[simulation_index][1][thisIndex] += 1
            if item[2] == "iron":
                break_count_by_simulation_list[simulation_index][2][thisIndex] += 1
        new_path = Path.split(".")[0] + "_failure.txt"
        with open(new_path, "w+") as handle:
            for index, item in enumerate(break_count_by_simulation_list[simulation_index][0]):
                parent = break_count_by_simulation_list[simulation_index]
                handle.write(('{},{},{}\n').format(parent[0][index], parent[1][index], parent[2][index]))
