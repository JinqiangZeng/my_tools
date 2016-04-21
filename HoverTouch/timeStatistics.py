from time import time

def time_cal(func):
    def callf(*args, **kwargs):
        start = time()
        r = func(*args, **kwargs)
        if len(args) > 0:
            print("Time elapsed {} {}s".format(args[0],time() - start))
        else:
            print("Time elapsed {} {}s".format(func.__name__,time() - start))
        return r
    return callf
