import os
f_ = open('2050_2099.txt', 'r')
f_list = f_.read().splitlines()
f_.close()

# f_list.pop(0)
lists = f_list.pop(0)
lists = lists.split('\t')
lists[0] = 'access1-0.1.rcp45'
to_write = dict()
tracking = list()
for item in lists:
    name = (item.split('.'))[0]
    rcp = item[-2:]
    if (rcp in to_write.keys()):
        to_write[rcp]['count'] += 1
    else:
        to_write[rcp] = {'count': 1, 'values': [], 'int_count': 0}
    tracking.append(rcp)

for item in f_list:
    vals = item.split('\t')
    vals.pop(0)
    for index, item in enumerate(vals):
        rcp = tracking[index]
        if (to_write[rcp]['int_count'] < to_write[rcp]['count']) and (len(to_write[rcp]['values']) != 0):
            to_write[rcp]['int_count'] += 1
            to_write[rcp]['values'][-1] += float(vals[index])
        else:
            to_write[rcp]['int_count'] = 1
            to_write[rcp]['values'].append(float(vals[index]))

for rcp in to_write.keys():
    f_ = open(('temp_output_2099/_{}_.txt').format(rcp), 'w+')
    for value in to_write[rcp]["values"]:
        f_.write(('{}\n').format(float(float(value) / to_write[rcp]['count'])))
    f_.close()
