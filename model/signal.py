from time import Time


class Signal(object):
    def __init__(self):
        self.link_id = None
        self.lane_type = None
        self.cycle_length = None
        self.green_start_time = None
        self.end_time = None

    def __repr__(self):
        return "link_id: %d, type: %s" % (self.link_id, self.lane_type)

    def is_green(self, relative_time):
        return self.green_start_time <= (Time().time + relative_time) % self.cycle_length <= self.end_time