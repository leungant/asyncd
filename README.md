# Asyncd

Python module for running functions and tasks async, to improve latency.

Designed for minimum effort for the end-user.

``` python
import asyncd
import time

def function_to_run(input):
    time.sleep(0.02)
    print(input)

# Get an async version of your function
a = asyncd.async(function_to_run)

for i in range(1000):
    a("Ran on separate thread")
```
