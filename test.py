#!/usr/bin/env python
import asyncd
from asyncd import async

import time
def slow_log(msg):
    time.sleep(0.1)
    print(msg)

@async
def slow_log_a(msg):
    time.sleep(0.1)
    print(msg)

asl  = asyncd.async(slow_log)

for i in range(199):
    print("%s" % i)
    #slow_log("slowlog %s" % i)
    asl("async slowlog: %s" % i)
    slow_log_a("async slowlog dec: %s" % i)
