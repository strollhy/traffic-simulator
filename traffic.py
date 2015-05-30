__author__ = 'hongyusong'


class Car():
    def __init__(self, data):
        self.car_id = data[0]     #车IDDD
        self.path = Path(data[1])
        self.start_time = data[2]
        self.distance = 0
        self.speed = 0
        self.arrive_time = []
        self.location = None


class Node():
    def __init__(self, data):
        self.node_id = data[0]
        self.link_id = data[1]
        self.left_light = data[2]
        self.right_light = data[3]
        self.through_light = data[4]
        self.time = data[5]             # TODO when to use it?

    def update(self, data):
        self.left_light, self.right_light, self.through_light = data


class Path():
    def __init__(self, od):
        self.od = [int(p) for p in od.split('-')]


class Link():
    def __init__(self, *args):
        self.link_id = 0
        self.nodes = {}
        self.left_link = 0
        self.right_link = 0
        self.through_link = 0

        self.length = 0
        self.num_of_cars = 0
        self.capacity = 0
        self.max_speed = 0
        self.min_speed = 0
        self.avg_speed = 0
        self.avg_density = 0

        self.sublink_1 = []
        self.sublink_2 = []
        self.left_lane = []
        self.right_lane = []
        self.through_lane = []