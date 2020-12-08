from helper import print_info
from time import process_time
from datetime import timedelta

def get_time_to_prnt(timestamp):
    return str(timedelta(seconds=timestamp))

class take_time:
    def __init__(self, name=None):
        self.name = name + '_' if name else ''

    def __call__(self, func):
        def wrapped_f(*args):
            _start = process_time()
            func(*args)
            _end = process_time()
            print_info("Took {} for {}".format(self.name + func.__name__, get_time_to_prnt(_end - _start)))
        return wrapped_f

class InlineTimer:
    def __init__(self, name=None):
        self.name = name if name else ''
        self._start = None

    def time(self):
        if self._start is None:
            self._start = process_time()
        else:
            _end = process_time()
            print_info("{}: {}s".format(self.name, get_time_to_prnt(_end - self._start)))
            self._start = None