class Signal(object):
    def __init__(self):
        self.link_id = None
        self.left_start = None
        self.through_start = None
        self.right_start = None
        self.left_period = None
        self.through_period = None
        self.right_period = None

    def __repr__(self):
        return "link_id: %d" % (self.link_id)