import numpy as np
import os

file1 = open(os.path.expanduser('8-31-17/noTime_yesCC_pvcPipeFail.txt'), 'r')
list1 = file1.read().splitlines()


file1.close()

yearList = list()
breakCount = list()
count = 0
while count < 83:
    yearList.append(count)
    breakCount.append(0)
    count += 1

for index, item in enumerate(list1):
    item = item.strip().split(' ')
    thisIndex = int(np.floor((int(item[1]) / 4380)))
    breakCount[thisIndex] = breakCount[thisIndex] + 1

for index, iteam in enumerate(breakCount):
    print(('{}').format(breakCount[index]))