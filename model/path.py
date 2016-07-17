class Path:
    def __init__(self):
        self.nodes = None
        self.car_num = None
        self.elapse_time = 0.0

    def __repr__(self):
        return "%s {%d}" % (self.__str__(), self.car_num)

    def __str__(self):
        return "-".join(str(n) for n in self.nodes)

    def avg_time(self):
        if not self.elapse_time:
            print "No elapse_time" + self
            return 1200
        else:
            return self.car_num / self.elapse_time
