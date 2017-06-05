#!/usr/bin/env python
''' Async. 

Run logging/any function on a separate thread/process so your main program can continue to run. Achieve with simple syntax:

ai = asyncd.async(fn)
# Thereafter, call ai as a function
ai('your inputs', 'here')

Program will wait for tasks to complete. This differs from the majority of modules in that no "wait()" call is required.



For example for logging on a separate thread:

import asyncd

def logging_fn(name, address):
    import time # be slow
    time.sleep(0.02) 
    print(name, address)

ai_log = asyncd.async(logging_fn)

for req in requests: 
    name, address = req['name'], req['address']
    print(name, address)
    ai_log(name, address)

The print statement will print immediately, ai_log will print with a delay. The program will wait until all requests are processed before exiting.



Suitable for e.g. C100 or other IO constrained problems which cause unnecessary server response delays due to blocks on expensive operations. For operations not requiring confirmation the main thread can continue to process requests while the task waits for the expensive process to complete in the background. 

After timeout (1 sec default) if there are no new operations requested, the thread is stopped, and another is recreated when next needed. The overhead to thread creation is usually several orders of magnitude less than most io operations so as to be minimal. 


Roadmap:

This version (1) improves latency. TODO add decorator.

Version 2: improve bandwidth with a threadpool, maybe processpool option

Version 3: await-able tasks (for operations that needed confirmation, but which you do not want the main thread to block), so e.g. futures/coroutines or callbacks

If you like the approach, feel free to work on the project!  '''

from __future__ import print_function

import time
import threading
from threading import Thread
import sys

if sys.version_info[0] < 3:
    from Queue import Queue
    from Queue import Empty as QUEUE_EMPTY

else:
    from queue import Empty as QUEUE_EMPTY
    from queue import Queue

import copy

def worker(q, fn, timeout):
    while True:
        try:
            #item = q.get(timeout=timeout)
            #fn(item)
            args, kwargs = q.get(timeout=timeout)
            fn(*args, **kwargs)
            q.task_done()
        except QUEUE_EMPTY as e: # catches timeout
            return


class async():
    def __init__(self, fn=print, queue_timeout=2, num_threads=1):
        self.q = Queue(maxsize=-1)
        self.fn = fn
        self.timeout = timeout
        self.num_threads = num_threads
        self._revive_thread()

    def _revive_thread(self):
        self.t = threading.Thread(target=worker, args=(self.q, self.fn, self.timeout))
        self.t.setDaemon(True)
        self.t.start()
        # print('\n\n\n %s \n\n' % fn.__name__)


    def __del__(self):
        # Waits for queue, thread to finish
        # print('in cleanup finalisation del')
        self.q.join()
        self.t.join()

    def call(self, *args, **kwargs):
        #print('in log %s %s' % (args, kwargs))
        if not self.t.isAlive():
            # print("Restarting thread and queue after timeout")
            self._revive_thread()
        #this_args, this_kwargs = copy.deepcopy(args), copy.deepcopy(kwargs) # paranoia induced by class and ref counting approach
        #self.q.put((this_args, this_kwargs))
        self.q.put((args, kwargs))
    __call__ = call

# Implement as decorator
# from pylru import lrudecorator
# @lrudecorator(10000) cant use decorator because attached goes out of scope! Ask Python maintainers for expected functionality.. seems inconsistent with function as a fc citizen.
# Does stay in scope if we use the FunctionCacheManager
# Tried functools approach but didn't seem the right choice in this scenario
import pylru
def asyncd(method, queue_timeout=0.1, num_threads=1):
    a = async(method, queue_timeout=queue_timeout, num_threads=num_threads) 
    return a
cached_asyncifys = pylru.FunctionCacheManager(asyncify, size=10000)



# TESTING. (for Auto: could write to files, compare file contents, file times)
def slow_log(input, wait):# , wait=0.001):
    time.sleep(wait) # 0.001)
    print("slow log %s %s" % (wait,input))

def slow_log_default(input, wait=0.01):# , wait=0.001):
    time.sleep(wait) # 0.001)
    print("slowlogdef %s %s " % (wait, input))


if __name__ == '__main__':
    print('Testing decorator functionality')
    @asyncd
    def slow_log_dec(msg, wait=0.04):
        print('called with wait %s' % wait)
        time.sleep(wait)
        print("slow_log_dec %s %s" % (wait, msg))
    slow_log_dec('hello from slow_log_dec')

    for i in range(100):
        print('triggered slow_log_dec %s' % i)
        slow_log_dec('hello from slow_log_dec %s' % i)
        slow_log_dec('hello from slow_log_dec %s' % i, 0.12)
    
    time.sleep(5)

    print('\n\n\nALog\n\n\n')
    al = async(slow_log, timeout=1)
    al('hello',3)
    time.sleep(2)

    for i in range(100):
        print('%s print' % i)
        al('%s asdf' % i, 0.02)

    time.sleep(2)
    # Test variable arguments
    al_def = async(slow_log_default, timeout=1)
    for i in range(100):
        print('%s print' % i)
        al_def('%s asdf' % i)
        al_def('%s asdf' % i, 0.03)

    for j in range(10):
        al('%s some bonus material' % j, wait=0.02)

    for i in range(100):
        print("printing %s as processing" % i)
        al_def(i)

    for j in range(100):
        print("printing j %s as processing" % j)
        al_def("j %s" % j)

    time.sleep(4)
    for k in range(100):
        print("printing k %s as processing" % k)
        al_def("k %s" % k)

    time.sleep(7)
    for l in range(100):
        print("printing l %s as processing" % l)
        al_def("l %s" % l)

    for i in range(100):
        print('triggered slow_log_dec %s' % i)
        slow_log_dec('hello from slow_log_dec %s' % i)
        slow_log_dec('hello from slow_log_dec %s' % i, 0.12)
