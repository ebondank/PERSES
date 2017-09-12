import os
import math


f_list = ['pvc', 'iron', 'pump']

for t_ in f_list:
    f_ = open(('{}_exposure_from_pdf.txt').format(t_), 'r')
    val_list = f_.read().splitlines()
    f_.close()

    f_ = open(('{}_redone_expose.txt').format(t_), 'w')
    c_s = 0
    v_t_w = 0
    for i in val_list:
        if (c_s < 50):
            v_t_w += float(i)
            c_s += 1
        else:
            f_.write(('{}\n').format(v_t_w))
            v_t_w = float(i)
            c_s = 1
    f_.close()
