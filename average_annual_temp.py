# f_ = open("temp_output/ccsm4_85.txt", 'r')
f_ = open("_85_.txt", 'r')
f_list = f_.read().splitlines()
f_.close()
f_list.pop(0)
i = 0
value = 0
for item in f_list:

    if (i % 365) == 0:
        print(value/365)
        value = float(item)
        i = 1
    else:
        i += 1
        value = value + float(item)
