import os
import math
import glob
import numpy as np

# dir_ = input("Where are the CSV files?\n")
dir_ = "component_cdf"
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
    prev_rows = [0]*30
    for j in range(8, l_):
        line_of_ages = line_list[j].split(',')
        for k in range(20, 50):
            # print(f"{line_of_ages[k-19]}\n")
            # input()
            if line_of_ages[k-19] in ["", " ", "\n"]: break
            cdf_val = float(line_of_ages[k - 19]) - float(prev_rows[k-20])
            prev_rows[k-20] = float(line_of_ages[k-19])
            bucket = (k * (j-8))
            if bucket in dict_list[comp_type][scenario].keys():
                dict_list[comp_type][scenario][bucket] += cdf_val
            else:
                dict_list[comp_type][scenario][bucket] = cdf_val

for t_ in dict_list.keys():
    for s_ in dict_list[t_].keys():
        d_c = 0
        with open(f"{dir_}/{t_}_{s_}_cdf.txt", 'w+') as handle:
            for b_ in dict_list[t_][s_].keys():
                d_c += (float(float(dict_list[t_][s_][b_])) / 30)
                handle.write(f'{d_c}\n')
