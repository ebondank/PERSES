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

epalib = ct.cdll.LoadLibrary('D:\\Austin_Michne\\1_11_17\\epanet2mingw64.dll')

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
ID = 105
time = ct.pointer(ct.c_long(1))
timestep = ct.pointer(ct.c_long(1))
print(epalib.ENsetlinkvalue(ct.c_int(5), ct.c_int(11), ct.c_float(0.0)))
# print(epalib.ENsetlinkvalue(ct.c_int(1), ct.c_int(12), ct.c_float(0.0)))
# while True:
i += 1
print('iter', i)

errorcode = epalib.ENrunH(time)
if errorcode != 0:
    print(4, 'ERRORCODE is', errorcode)
print('TIME is', time.contents.value)

nodeid = ct.c_char_p(str(ID).encode('utf-8'))
nodeidx = ct.pointer(ct.c_int(0))
nodevalue = ct.pointer(ct.c_float(0.0))

errorcode = epalib.ENgetnodeindex(nodeid, nodeidx)
if errorcode != 0:
    print(5, 'ERRORCODE is', errorcode)
print('NODEID', nodeid.value.decode('utf-8'),
      'has NODEIDX', nodeidx.contents.value)

errorcode = epalib.ENgetnodevalue(
    nodeidx.contents, ENnodeparam.BASEDEMAND, nodevalue)
if errorcode != 0:
    print(6, 'ERRORCODE is', errorcode)
print('EN_BASEDEMAND is', nodevalue.contents.value)

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



# ENcloseH() may belong here

print('---------------\n')
errorcode = epalib.ENclose()
if errorcode != 0:
    print(9, 'ERRORCODE is', errorcode)
print('')
