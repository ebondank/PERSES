import sqlite3 as sql
import math
import os

Path = '8-23-17/real_rcp45/noTemp0.db'
print(Path)
db = sql.connect(Path)
com = db.cursor()
component = 'pump'

list_of_failures = com.execute(('SELECT * FROM failureData WHERE componentType = "pump" ORDER BY Bihour_Count ASC'))

dict_of_ages = dict()
dict_of_lifetimes = dict()

for index, item in enumerate(list_of_failures):
    if (item[1] in dict_of_ages.keys()):
        dict_of_ages[item[1]].append(item[0])
        length_of_arr = len(dict_of_ages[item[1]])
        dict_of_lifetimes[item[1]].append(dict_of_ages[item[1]][length_of_arr - 1] - dict_of_ages[item[1]][length_of_arr - 2])


    else:
        dict_of_ages[item[1]] = [item[0]]
        dict_of_lifetimes[item[1]] = []

for item in dict_of_lifetimes.keys():
    for itm in dict_of_lifetimes[item]:
        print(itm)
    print('\n\n\n')