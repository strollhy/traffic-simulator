class SubLink(object):
    def __init__(self, link, lane_num):
        self.link = link
        self.lanes = [[] for _ in xrange(lane_num)]

    def __repr__(self):
        return "link: %s, lanes: %s" % (self.link, self.lanes)

    def get_car_num(self):
        return sum([len(l) for l in self.lanes])