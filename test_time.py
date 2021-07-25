"""this file has a decorator function that checks the execution timing of other functions"""
from time import time
def timeit(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function has been executed in {round(t2-t1, 2)} seconds')
        return result
    return wrapper