import os
import math
import numpy as np

file_list = ['pump_cdf.txt', 'pvc_cdf.txt', 'iron_cdf.txt']
dict_list = {'pump': {}, 'pvc': {}, 'iron': {}}

for f_ in file_list:
    line_f = open(f_, 'r')
    line_list = line_f.read().splitlines()
    line_f.close()

    comp_type = f_.split('_')[0]
    l_ = len(line_list)

    for j in range(0, l_):
        line_of_ages = line_list[j].split('\t')
        for k in range(20, 50):
            cdf_val = float(line_of_ages[k - 20])
            bucket = (k * (j))
            if bucket in dict_list[comp_type].keys():
                dict_list[comp_type][bucket] += cdf_val
            else:
                dict_list[comp_type][bucket] = cdf_val

for t_ in dict_list.keys():
    f_o = open(('{}_exposure_from_pdf.txt').format(t_), 'w')
    for b_ in dict_list[t_].keys():
        f_o.write(('{}\n').format(dict_list[t_][b_]))
    f_o.close()

