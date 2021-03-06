# Built using Python 3.6.0
import ctypes as ct


class ENnodeparam(object):  # different for SOURCES
    ELEVATION = ct.c_int(0)
    BASEDEMAND = ct.c_int(1)
    PATTERN = ct.c_int(2)
    EMITTER = ct.c_int(3)
    INITQUAL = ct.c_int(4)
    SOURCEQUAL = ct.c_int(5)
    SOURCEPAT = ct.c_int(6)
    SOURCETYPE = ct.c_int(7)
    TANKLEVEL = ct.c_int(8)
    DEMAND = ct.c_int(9)
    HEAD = ct.c_int(10)
    PRESSURE = ct.c_int(11)
    QUALITY = ct.c_int(12)
    SOURCEMASS = ct.c_int(13)


class ENlinkparam(object):
    DIAMETER = ct.c_int(0)
    LENGTH = ct.c_int(1)
    ROUGHNESS = ct.c_int(2)
    MINORLOSS = ct.c_int(3)
    INITSTATUS = ct.c_int(4)
    INITSETTING = ct.c_int(5)
    KBULK = ct.c_int(6)
    KWALL = ct.c_int(7)
    FLOW = ct.c_int(8)
    VELOCITY = ct.c_int(9)
    HEADLOSS = ct.c_int(10)
    STATUS = ct.c_int(11)
    SETTING = ct.c_int(12)
    ENERGY = ct.c_int(13)

epalib = ct.cdll.LoadLibrary('D:\\Austin_Michne\\1_11_17\\epanet2.dll')

# Python strings
a = 'north_marin_c.inp'
b = 'zz.rpt'
c = ''

# Byte objects
b_a = ct.c_char_p(a.encode('utf-8'))
b_b = ct.c_char_p(b.encode('utf-8'))
b_c = ct.c_char_p(c.encode('utf-8'))

# Send strings as char* to the epalib function
errorcode = epalib.ENopen(b_a, b_b, b_c)
if errorcode != 0:
    print(1, 'ERRORCODE is', errorcode)

errorcode = epalib.ENopenH()
if errorcode != 0:
    print(2, 'ERRORCODE is', errorcode)

init_flag = ct.c_int(0)
errorcode = epalib.ENinitH(init_flag)
if errorcode != 0:
    print(3, 'ERRORCODE is', errorcode)
print('\n---------------\n')

i = 0
ID = 60
time = ct.pointer(ct.c_long(0))
timestep = ct.pointer(ct.c_long(7200))
# print(epalib.ENsetlinkvalue(ct.c_int(5), ct.c_int(11), ct.c_float(1.0)))
# print(epalib.ENsetlinkvalue(ct.c_int(1), ct.c_int(12), ct.c_float(0.0)))
# while True:
i += 1
print('iter', i)
while True:
    errorcode = epalib.ENrunH(time)
    if errorcode != 0:
        print(4, 'ERRORCODE is', errorcode)
    print('TIME is', time.contents.value)
    indexReturn1 = ct.pointer(ct.c_int(0))
    # For the first pipe out of pump 10
    linkID = ct.c_char_p(str(335).encode('utf-8'))
    print(epalib.ENgetlinkindex(linkID, indexReturn1))

    if (time.contents.value == 0):
        print(epalib.ENsetlinkvalue(indexReturn1.contents, ct.c_int(11), ct.c_float(0.0)))
        testing = ct.pointer(ct.c_int(11))
        print(epalib.ENgetlinktype(indexReturn1.contents, testing))
        print(testing.contents.value)
    else:
        print(epalib.ENsetlinkvalue(indexReturn1.contents, ct.c_int(11), ct.c_float(1.0)))

    nodeid = ct.c_char_p(str(131).encode('utf-8'))
    nodeidx = ct.pointer(ct.c_int(0))
    nodevalue = ct.pointer(ct.c_float(0.0))

    errorcode = epalib.ENgetnodeindex(nodeid, nodeidx)
    if errorcode != 0:
        print(5, 'ERRORCODE is', errorcode)
    print('NODEID', nodeid.value.decode('utf-8'),
          'has NODEIDX', nodeidx.contents.value)

    errorcode = epalib.ENgetnodevalue(
        nodeidx.contents, ENnodeparam.PRESSURE, nodevalue)
    if errorcode != 0:
        print(7, 'ERRORCODE is', errorcode)
    print('EN_DEMAND is', nodevalue.contents.value)

    errorcode = epalib.ENnextH(timestep)
    if errorcode != 0:
        print(8, 'ERRORCODE is', errorcode)
    print('TIMESTEP is', timestep.contents.value)
    print('')

    if (time.contents.value == 86400):
        print('Failure method finished')
        break

# ENcloseH() may belong here

print('---------------\n')
errorcode = epalib.ENclose()
if errorcode != 0:
    print(9, 'ERRORCODE is', errorcode)
print('')
