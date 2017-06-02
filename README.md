# Asyncd

Python module for running functions and tasks async, to improve latency.

Designed for the end-user.

``` python
import asyncd

def function_to_run(inputs):
    for this_input in inputs:
        expensive_function_to_run(this_input)

# Get an async version of your function
a = asyncd.async(function_to_run)

for i in range(1000):
    a("Ran on separate thread %s" % i)
```
