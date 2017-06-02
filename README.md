# Asyncd

Python module for running functions and tasks async, to improve latency.

Designed for minimum effort for the end-user.

``` python
import asyncd
def function_to_run("input"):
    print(input)
a = asyncd.async(function_to_run)

a("Ran on separate thread")
```
