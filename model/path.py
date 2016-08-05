class Path:
    def __init__(self):
        self.nodes = None
        self.car_num = None
        self.elapse_time = 0.0
        self.elapse_time_section = [[] for _ in xrange(8)]

    def __repr__(self):
        return "%s {%d}" % (self.__str__(), self.car_num)

    def __str__(self):
        return "-".join(str(n) for n in self.nodes)

    def avg_time(self):
        if not self.car_num:
            print "No car reaches destination on path %s" % self
            return 200
        else:
            return self.elapse_time / self.car_num

    def avg_section_cost(self, section):
        return (sum(self.elapse_time_section[section])) / (len(self.elapse_time_section[section]) + .1)