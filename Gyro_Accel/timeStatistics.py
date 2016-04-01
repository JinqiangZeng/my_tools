from time import time

def time_cal(func):
    def callf(*args, **kwargs):
        start = time()
        r = func(*args, **kwargs)
        print("{} {}s".format(func.__name__ ,time() - start))
        return r
    return callf
