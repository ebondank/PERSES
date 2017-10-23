import os
f_ = open('2015_2050.txt', 'r')
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
    if (name in to_write.keys()):
        if (rcp in to_write[name].keys()):
            to_write[name][rcp]['count'] += 1
        else:
            to_write[name][rcp] = {'count': 1, 'values': [], 'int_count': 0}
    else:
        to_write[name] = {rcp: {'count': 1, 'values': [], 'int_count': 0}}
    tracking.append([name, rcp])

for item in f_list:
    vals = item.split('\t')
    vals.pop(0)
    for index, item in enumerate(vals):
        name = tracking[index][0]
        rcp = tracking[index][1]
        if (to_write[name][rcp]['int_count'] < to_write[name][rcp]['count']) and (len(to_write[name][rcp]['values']) != 0):
            to_write[name][rcp]['int_count'] += 1
            to_write[name][rcp]['values'][-1] += float(vals[index])
        else:
            to_write[name][rcp]['int_count'] = 1
            to_write[name][rcp]['values'].append(float(vals[index]))

for name in to_write.keys():
    for rcp in to_write[name].keys():
        f_ = open(('temp_output/{}_{}.txt').format(name, rcp), 'w+')
        for value in to_write[name][rcp]["values"]:
            f_.write(('{}\n').format(float(float(value) / to_write[name][rcp]['count'])))
        f_.close()
