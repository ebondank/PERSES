import sqlite3 as sql
import math
import numpy as np
import os


class component_populations(object):
    
    def __init__(self, temp_curve_file, failure_dist_file, component_type, component_god_factor_list, amount, db_cur, table_name):
        self.component_type = component_type
        self.db_cur = db_cur
        self.table_name = table_name
        self.god_factor_list = component_god_factor_list
        self.god_factor_count = [0] * len(self.god_factor_list)
        self.biHourToYear = .0002283105022831050228310502283105
        f_ = open(temp_curve_file, 'r')
        f_list = f_.read().expandtabs().splitlines()
        new_list = list()
        for index, item in enumerate(f_list):
            if len(item.split(' ')) != (1 or 0):
                for item_split in item.split():
                    try:
                        new_list.append(float(item_split))
                    except ValueError as val:
                        print(item_split)
            else:
                new_list.append(item)
        f_.close()
        self.temp_curve = new_list

        f_ = open(failure_dist_file, 'r')
        f_list = f_.read().expandtabs().splitlines()
        
        f_.close()
        new_list = list()
        for index, item in enumerate(f_list):
            if len(item.split(' ')) != (1 or 0):
                for item_split in item.split():
                    try:
                        new_list.append(float(item_split))
                    except ValueError as val:
                        print(item_split)
            else:
                new_list.append(item)
        self.distribution_list = new_list
        self.exposure_array = list()
        count = 0
        while (count < amount):
            self.exposure_array.append(0)
            count += 1
    

    def failure_evaluation(self, index, time, component_type):
        per_failed1 = self.distribution_list[math.floor(float(self.exposure_array[index]))]
        per_failed2 = self.distribution_list[math.ceil(float(self.exposure_array[index]))]
        per_failed = (float(per_failed2) - float(per_failed1)) * (float(self.exposure_array[index]) - math.floor(float(self.exposure_array[index]))) + float(per_failed1)

        if (per_failed > self.god_factor_list[index][self.god_factor_count[index]]):
            self.db_cur.execute(('''INSERT INTO {} VALUES (?, ?, ?)''').format(self.table_name), (time, index, component_type))
            self.exposure_array[index] = 0
            self.god_factor_count[index] += 1
        else:
            self.exposure_array[index] = self.exposure_array[index] + (self.biHourToYear * float(self.temp_curve[math.floor(time/12)]))
            

if __name__ == "__main__":
    db_table_list = ["histTasMaxBD", "tasMaxBD", "tasMaxBD85"]
    try:
        os.remove("statistics.db")
    except Exception as exp:
        print('No database here')

    db_obj = sql.connect("statistics.db")
    db_cur = db_obj.cursor()

    for item in db_table_list:
        db_cur.execute(('''CREATE TABLE {} (Bihour_Count real, NodeID real, componentType real)''').format(item))
    
    pop_list = ["pump", "pvc", "iron"]
    god_factor_simulation_syncing = [list(), list(), list()]
    component_count = 250
    count = 0

    # {"pump": [1, .2, .6], etc.}
    while (count < component_count):
        random_list = list(np.random.uniform(0, 1, 1000))
        for index, item in enumerate(pop_list):
            god_factor_simulation_syncing[index].append(random_list)
        count += 1
    for simulation in db_table_list:
        statistics_dict = dict()
        for index, item in enumerate(pop_list):
            temp_curve = ("{}.txt").format(simulation)
            cdf_curve = ("{}_made_cdf.txt").format(item)
            gf = god_factor_simulation_syncing[index]
            new_simulation = component_populations(temp_curve, cdf_curve, item, gf, component_count, db_cur, simulation)
            statistics_dict[("{}_{}").format(simulation, item)] = new_simulation
            print(item)
        time = 0
        goal_time = 350000
        while time < goal_time:
            for population in statistics_dict.keys():
                index = 0
                while index < component_count:
                    component_type = list(population.split('_'))[1]
                    statistics_dict[population].failure_evaluation(index, time, component_type)
                    index += 1
            time += 1
    db_obj.commit()
    db_obj.close()
