import numpy as np
import os
import sqlite3 as sql

# file1 = open(os.path.expanduser('8-08-17/noTime_yesCC_ironPipeFail.txt'), 'r')
# list1 = file1.read().splitlines()
Path = 'statistics 10-16-17.db'
db = sql.connect(Path)
com = db.cursor()

yearList = list()
breakCountpvc = list()
breakCountiron = list()
breakCountpump = list()
db_table_list = ["histTasMaxBD", "tasMaxBD", "tasMaxBD85"]
break_count_by_simulation_list = list()
for simulation_index, simulation in enumerate(db_table_list):
    count = 0
    break_count_by_simulation_list.append([list(), list(), list()])
    while count < 83:
        break_count_by_simulation_list[simulation_index][0].append(0)
        break_count_by_simulation_list[simulation_index][1].append(0)
        break_count_by_simulation_list[simulation_index][2].append(0)
        count += 1

count = 0
while count < 83:
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


    print('\n\n\n')
    for index, iteam in enumerate(break_count_by_simulation_list[simulation_index][0]):
        print(('{}').format(break_count_by_simulation_list[simulation_index][0][index]))
    print('\n\n\n')
    for index, iteam in enumerate(break_count_by_simulation_list[simulation_index][1]):
        print(('{}').format(break_count_by_simulation_list[simulation_index][1][index]))
    print('\n\n\n')
    for index, iteam in enumerate(break_count_by_simulation_list[simulation_index][2]):
        print(('{}').format(break_count_by_simulation_list[simulation_index][2][index]))
