class Time(object):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Time, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_time'):
            setattr(self, '_time', 0)

    @property
    def time(self):
        return self._time

    def update_time(self):
        self._time += 1
