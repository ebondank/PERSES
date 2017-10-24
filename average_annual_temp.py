f_ = open("csiromk85.txt", 'r')
f_list = f_.read().splitlines()
f_.close()

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
