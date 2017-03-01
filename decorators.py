from datetime import datetime
from functools import wraps


def benchmark(func):
    # @wraps
    def accepter(*args, **kwargs):
        before = datetime.now()
        res = func(*args, **kwargs)
        after = datetime.now()
        print('{} took {} microseconds'.format(func.__name__, (after - before).microseconds))
        return res
    return accepter
