import time

class take_time:
    def __init__(self, func, name=None):
        self.func = func
        self.name = " '"  + name + "'" if name else ''

    def __call__(self):
        self._start = time.time()
        self.f()
        self._end = time.time()
        print_info("Took {} for {}".format(self._end - self._start, self.func.__name__ + "_" + self.name))

class InlineTimer:
    def __init__(self, name=None):
        self.name = " '"  + name + "'" if name else ''
        self._start = None

    def time(self):
        if self._start is None:
            self._start = time.time()
        else:
            _end = time.time()
            print_info("Took {} for {}".format(_end - self._start, self.name))
