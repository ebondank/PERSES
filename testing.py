import math
import os
import sqlite3 as sql
from decimal import Decimal
import numpy as np
from epanet import epanet
from ctypes import cdll

epalib = cdll.LoadLibrary('D:\\Austin_Michne\\1_11_17\\epanet2mingw64.dll')
handle = epalib._handle
cdll.dlclose()