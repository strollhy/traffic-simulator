class SubLink(object):
    def __init__(self, link, lane_num):
        self.link = link
        self.lanes = [[] for _ in xrange(lane_num)]

    def __repr__(self):
        return "Lanes: %s" % (self.lanes)

    @property
    def car_num(self):
        return sum([len(l) for l in self.lanes])