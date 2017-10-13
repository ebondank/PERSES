import sqlite3 as sql
import math
import numpy as np
import os


class component_populations:
    exposure_array = list()
    temp_curve = list()
    distribution_list = list()
    god_factor_list = list()
    component_type = None
    biHourToYear = float(.0002283105022831050228310502283105)
    db_cur = None


    def __init__(self, temp_curve_file, failure_dist_file, component_type, amount, db_cur):
        self.component_type = component_type
        self.db_cur = db_cur
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

        count = 0
        while (count < amount):
            self.god_factor_list.append(float(np.random.uniform(0, 1)))
            self.exposure_array.append(0)
            count += 1
    

    def failure_evaluation(self, index, time):
        per_failed1 = self.distribution_list[math.floor(float(self.exposure_array[index]))]
        per_failed2 = self.distribution_list[math.ceil(float(self.exposure_array[index]))]
        per_failed = (float(per_failed2) - float(per_failed1)) * (float(self.exposure_array[index]) - math.floor(float(self.exposure_array[index]))) + float(per_failed1)

        if (per_failed > self.god_factor_list[index]):
            self.db_cur.execute('''INSERT INTO failureData VALUES (?, ?, ?)''', (time, index, self.component_type))
            self.exposure_array[index] = 0
        else:
            try:
                self.exposure_array[index] = self.exposure_array[index] + (self.biHourToYear * float(self.temp_curve[math.floor(time/12)]))
            except IndexError as idx:
                print(time)
                print(self.temp_curve[time-1])
                print(self.exposure_array[index-1])
                print(index)
                print(self.exposure_array[index])
                exit()

if __name__ == "__main__":
    db_cur_list_labels = ["histTasMaxBD", "tasMaxBD", "tasMaxBD85"]
    db_cur_list = list()
    db_obj_list = list()
    for item in db_cur_list_labels:
        try:
            os.remove(("{}.db").format(item))
        except Exception as exp:
            print('No database here')
        db_obj = sql.connect(("{}.db").format(item))
        db_cur = db_obj.cursor()
        db_cur.execute('''CREATE TABLE failureData (Bihour_Count real, NodeID real, componentType real)''')
        db_cur_list.append(db_cur)
        db_obj_list.append(db_obj)

    
    pop_list = ["pvc", "pump", "iron"]
    for simulation_index, simulation in enumerate(db_cur_list):
        statistics_list = list()
        for index, item in enumerate(pop_list):
            statistics_list.append(component_populations(("{}.txt").format(db_cur_list_labels[index]), \
                ("{}_made_cdf.txt").format(item), pop_list[index], 1, simulation))
            print(item)
        time = 0
        goal_time = 350000
        print(pop_list)
        while time < goal_time:
            for population in statistics_list:
                for index, value in enumerate(population.god_factor_list):
                    population.failure_evaluation(index, time)
            time += 1
        db_obj_list[simulation_index].commit()
        db_obj_list[simulation_index].close()
