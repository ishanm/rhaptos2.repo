

'''

'''
import socket
import time
import random

CARBON_SERVER = 'log.frozone.mikadosoftware.com'
CARBON_PORT = 2003
STATSD_PORT = 8125
STATSD_HOST = CARBON_SERVER

import statsd 

def test_statsd():

    c = statsd.StatsClient(STATSD_HOST, STATSD_PORT)
    for i in range(1000):
        c.incr('rhaptos2.statsd.verify') 

if __name__ == '__main__':
    test_statsd()
