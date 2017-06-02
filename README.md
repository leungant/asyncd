# Asyncd

Python module for speeding up application responsiveness by asynchronously running functions.


Designed for the end-user.

``` python
import asyncd, time

def expensive_function_to_run(input):
    time.sleep(0.02)
    print(input)

# Get an async version of your function
a = asyncd.async(expensive_function_to_run)

for i in range(1000):
    a("Ran on separate thread %s" % i)
```
