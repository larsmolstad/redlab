import time
from ctypes import *
import platform

if platform.architecture()[0] == '32bit':
    cbw = windll.cbw32  
else:
    cbw = windll.cbw64 

# Gain [-10 10] [-5 5] [-2 2] [-1 1]
#            1      0     14      4

maxv_codes = {10 : 1,
              5 : 0,
              2 : 14,
              1 : 4}


def to_engunits(x):
    engunits = c_float()
    cbw.cbToEngUnits(0, 0, x, byref(engunits))
    return engunits


def read_channel(n):
    x = c_int()
    cbw.cbAIn(0, c_int(n), 0, byref(x))
    engunits = to_engunits(x)
    return engunits.value, x


def read_channel_voltage(n, max_absV = 10):
    x = c_int()
    n = c_int(n)
    gain = c_int(maxv_codes[max_absV])
    engunits = c_float()
    cbw.cbVIn(0, n, gain, byref(engunits), 0)
    # for double: eng = c_double();cbw.cbVIn32(0, n, gain, byref(eng), 0);eng.value
    #(boardnum, chan, gain, output, options)
    return engunits.value


def average_voltage(n=0, m=1, t=0.01):
    """ Reads from channel n
    averaging over m readings,
    sleeping t seconds between each"""
    x = read_channel(n)
    for i in range(m-1):
        time.sleep(t)
        x = x + read_channelV(n)
    x = x*1.0/m
    return x


def test(value, confport=0, outport=1):
    a = cbw.cbDConfigPort(0, c_int(confport), c_ushort(value))
    b = cbw.cbDOut(0, c_int(outport), c_uint8(value))
    return a, b


cbw.cbErrHandling(3,0)
