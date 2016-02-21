class Path:
    def __init__(self, nodes, car_num):
        self.nodes = nodes
        self.car_num = car_num
        self.elapse_time = 0.0

    def avg_time(self):
        if not self.elapse_time:
            return 10
        return self.car_num / self.elapse_time