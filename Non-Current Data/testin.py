import math

# f = open('7-4-17/real_pvcPipeFail.txt', 'r')
# fR = f.read().splitlines()
# f.close()
# i = 0

# list1 = list()
# while i < 83:
#     list1.append(0)
#     i += 1
# for item in fR:
#     i = math.floor(float(item.split(' ')[1]) / 4960)
#     list1[i] = float(list1[i]) + 1

# f2 = open('testing.txt', 'w')
# for item in list1:
#     f2.write(('{}\n').format(item / 365))
# f2.close()
# f = open('histTasMaxBD.txt', 'r')
# fList = f.read().splitlines()
# f.close()
# listOfHistTemp = list()
# histCount = 0


# for line in fList:
#     if ((histCount % 365) == 0):
#         listOfHistTemp.append(float(0))
#     listOfHistTemp[math.floor((histCount / 365))] = listOfHistTemp[math.floor((histCount / 365))] + float(line)
#     histCount += 1

# fOut = open('histOut.txt', 'w')
# for item in listOfHistTemp:
#     fOut.write(str(item / 365) + "\n")
# fOut.close()

# m = .0002
# b = 29.793
# m = .00003
# b = 29.324
# count = 0

histTempFile = open('histTasMaxBD.txt', 'r')
histTempList = histTempFile.read().splitlines()
histTempFile.close()
formTas = open("generatedTasMaxHist.txt", "w")

newTempList = list()
for item in histTempList:
    if ((float(item) * 1.75) < 50):
        formTas.write(('{}\n').format(float(item) * 1.75))
    else:
        formTas.write('50\n')


# while count < 31025:
#     tempToWrite = m * count + b
#     formTas.write(("{}\n").format(tempToWrite))
#     count += 1
formTas.close()