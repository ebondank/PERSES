import os
import math
import glob
import numpy as np


# file_list = ['pump_cdf.txt', 'pvc_cdf.txt', 'iron_cdf.txt']
# file_list = ['new_cdf/mid_elec.txt', 'new_cdf/mid_case_motor.txt']
dir_ = input("Where are the CSV files?\n")
file_list = glob.glob(dir_ + "/*.csv")
file_name_list = [x.split("/")[1] for x in file_list]
print(file_list)
dict_list = {'iron': {}, 'pvc': {}, 'elec': {}, 'motor': {}}

for idx_, f_ in enumerate(file_name_list):
    line_f = open(file_list[idx_], 'r')
    line_list = line_f.read().splitlines()
    line_f.close()

    # comp_type = f_.split('_')[0]
    tmp = f_.split('_')
    scenario = tmp[0]
    tmp = tmp[1].split('.')
    comp_type = tmp[0]
    dict_list[comp_type][scenario] = dict()
    l_ = len(line_list)

    for j in range(8, l_):
        line_of_ages = line_list[j].split(',')
        for k in range(20, 51):
            if line_of_ages[k-19] in ["", " ", "\n"]: break
            cdf_val = float(line_of_ages[k - 19])
            bucket = (k * (j))
            if bucket in dict_list[comp_type][scenario].keys():
                dict_list[comp_type][scenario][bucket] += cdf_val
            else:
                dict_list[comp_type][scenario][bucket] = cdf_val

for t_ in dict_list.keys():
    for s_ in dict_list[t_].keys():
        d_c = 0
        with open((dir_ + '/{}_{}_cdf.txt').format(t_, s_), 'w+') as handle:
            for b_ in dict_list[t_][s_].keys():
                d_c += float(dict_list[t_][s_][b_] / 30)
                handle.write(('{}\n').format(d_c))
