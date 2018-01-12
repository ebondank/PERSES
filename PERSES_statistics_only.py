import sqlite3 as sql
import math
import numpy as np
import os
import inquirer
import threading
import multiprocessing as mp

def input_file_cleaning(filename):
    ret_list = list()
    if not isinstance(filename, list):
        filename = [filename]
    for _f in filename:
        with open(_f, 'r') as x:
            y = x.read().expandtabs().splitlines()
            for z in y:
                if len(z.split(' ')) > 1:
                    for q in z.split():
                        try:
                            ret_list.append(float(q))
                        except ValueError as val:
                            print(val)
                            input()
                else:
                    try:
                        ret_list.append(float(z))
                    except ValueError as val:
                        print(val)
    return ret_list

class component_populations(object):
    
    def __init__(self, temp_curve_file, failure_dist_files, component_type, component_god_factor_list, component_count, goal_time, starting_index, ending_index, thread_splice, slice_size):
        self.component_type = component_type
        self.god_factor_lists = component_god_factor_list
        self.biHourToYear = .0002283105022831050228310502283105
        self.biHour_counter = 0
        self.day_count = 0
        self.index = 0
        self.component_count = component_count - 1
        self.failure_instances = []
        self.thread_splice = thread_splice
        self.goal_time = goal_time
        self.starting_index = starting_index
        self.ending_index = component_count - (slice_size * thread_splice)
        if isinstance(temp_curve_file, str):
            self.temp_curve = input_file_cleaning(temp_curve_file)
        elif isinstance(temp_curve_file, list):
            self.temp_curve = temp_curve_file
        if (not isinstance(failure_dist_files, list)) or (all(isinstance(x, float) for x in failure_dist_files)):
            failure_dist_files = [failure_dist_files]
        if all(isinstance(elem, str) for elem in failure_dist_files):
            self.distribution_lists = list()
            for failure_dist_file in failure_dist_files: 
                self.distribution_lists.append(input_file_cleaning(failure_dist_file))
        
        elif all(isinstance(elem, list) for elem in failure_dist_files):
            self.distribution_lists = failure_dist_files
        self.exposure_arrays = [[0]*component_count]*len(self.distribution_lists)
        self.god_factor_counts = [[0]*component_count]*len(self.distribution_lists)

    def failure_evaluation(self):
        if self.index >= self.ending_index:
            self.index = self.starting_index
            # self.biHour_counter += 1
            self.day_count += 1
        for idx, dist in enumerate(self.distribution_lists):
            # print(math.floor(self.exposure_arrays[index][self.index]))
            per_failed1 = dist[math.floor(self.exposure_arrays[idx][self.index])]
            per_failed2 = dist[math.ceil(self.exposure_arrays[idx][self.index])]
            per_failed = (per_failed2 - per_failed1) * (self.exposure_arrays[idx][self.index] - \
                 math.floor(self.exposure_arrays[idx][self.index])) + per_failed1
            if (per_failed > self.god_factor_lists[idx][self.index][self.god_factor_counts[idx][self.index]]):
                self.failure_instances.append(("{}|{}|{}|{}|{}|{}|{}").format(self.day_count, \
                    self.index, self.component_type, self.thread_splice,\
                    self.god_factor_lists[idx][self.index][self.god_factor_counts[idx][self.index]], \
                    self.exposure_arrays[idx][self.index], self.god_factor_counts[idx][self.index]))
                # print(self.failure_instances[-1])
                for x in range(0, len(self.distribution_lists)):
                    self.exposure_arrays[x][self.index] = 0
                    self.god_factor_counts[x][self.index] += 1
            else:
                self.exposure_arrays[idx][self.index] = self.exposure_arrays[idx][self.index] + \
                    float(self.temp_curve[self.day_count] / 365)
        else:
            self.index += 1



    def thread_looping(self):
        while (self.biHour_counter < self.goal_time):
            self.failure_evaluation()
        return self.failure_instances


if __name__ == "__main__":
    # questions = [
    # inquirer.List('size',
                    # message="Which temperature would you like to use?",
                    # choices=["rcp85_1950_2100", "rcp45_1950_2100"],
                # ),]
    # temp_scenarios = [(inquirer.prompt(questions))['size']]
    temp_scenarios = ["rcp85_1950_2100"]

    pop_list = ["pump", "pvc", "iron"]
    god_factor_list = [["mid_case_motor.txt", "mid_case_elec.txt"],\
                        ["pvc_made_cdf.txt"], ["iron_made_cdf.txt"]]
    component_count_dict = {"pump": 113, "pvc": 30750, "iron": 30750}
    process_list = []
    goal_time = 54000

    god_factor_simulation_syncing = list()
    for index, sim in enumerate(pop_list):
        god_factor_simulation_syncing.append(list())
        for x in range(0, len(max(god_factor_list, key=len))):
            god_factor_simulation_syncing[index].append(list())
            count = 0
            while count < component_count_dict[sim]:
                god_factor_simulation_syncing[index][x].append(np.ndarray.tolist(np.random.random(100)))
                count += 1

    # q = mp.Queue()
    for simulation in temp_scenarios:
        statistics_dict = dict()
        temp_curve = ("{}.txt").format(simulation)
        cdf_curves = list()
        cdf_file_data = list()
        temperature_data = input_file_cleaning(temp_curve)
        for index, item in enumerate(pop_list):
            # if (os.name != "nt"):
            cdf_curves.append(god_factor_list[index])
            cdf_file_data.append(input_file_cleaning(god_factor_list[index]))
                    
            # else:
                # cdf_curve = (os.path.relpath('new_cdf\\{}_made_cdf.txt').format(item))
            gf = god_factor_simulation_syncing[index]
            temp_comp_count = component_count_dict[item]
            # slice_size = math.floor(component_count_dict[item] / mp.cpu_count())
            slice_size = 35000
            thread_splice_count = 0
            new_simulation = list()
            while (temp_comp_count > 0):
                if temp_comp_count > slice_size:
                    new_simulation.append(component_populations(temperature_data,\
                        cdf_file_data[index], item, \
                        gf, component_count_dict[item], goal_time, \
                        temp_comp_count - slice_size, temp_comp_count, \
                        thread_splice_count, slice_size))
                else:
                    new_simulation.append(component_populations(temperature_data,\
                        cdf_file_data[index], item,\
                        gf, component_count_dict[item], goal_time,\
                        0, temp_comp_count, thread_splice_count, slice_size))
                temp_comp_count -= slice_size
                thread_splice_count += 1
                
            statistics_dict[("{}_{}").format(simulation, item)] = {"sims": new_simulation, "type": item, "process_list":[]}
            for sim in statistics_dict[("{}_{}").format(simulation, item)]['sims']:
                process_list.append(sim)
            print(item)
    # mp.Semaphore(mp.cpu_count())
    pool = mp.Pool(mp.cpu_count())
    failures = pool.imap(component_populations.thread_looping, process_list)
    pool.close()
    pool.join()

    with open('test_multiProc_out.txt', 'w') as testHand:
        for x in failures:
            for y in x:
                testHand.write(("{}\n").format(y))