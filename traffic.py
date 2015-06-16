__author__ = 'hongyusong'


class Car():
    def __init__(self, data):
        self.car_id = data[0]
        self.path = data[1]
        self.start_time = data[2]
        self.distance = 0
        self.speed = 0
        self.arrive_time = []
        self.location = None


class Light():
    def __init__(self, red_period, green_period, light=0):
        self.red_period = red_period
        self.green_period = green_period
        self.light = light

    def clone(self):
        return Light(self.red_period, self.green_period, self.light)

    def reverse_clone(self):
        return Light(self.green_period, self.red_period, 1 - self.light)

    def update_status(self):
        pass


class Link():
    def __init__(self, *args):
        self.link_id = ()
        self.left_link = 0
        self.right_link = 0
        self.through_link = 0
        self.length = 0
        self.num_of_lanes=0
        self.num_of_cars = 0
        self.capacity = 0
        self.max_speed = 0
        self.min_speed = 0
        self.avg_speed = 0
        self.avg_density = 0
        self.sublink_1 = [] #Cars in Sublink1
        self.sublink_2 = [] #Cars in Sublink2
        self.left_lane = [] #cars in the last left lane
        self.right_lane = [] #cars in the last right lane
        self.through_lane = [] #cars in the last through lane
        self.lights = []

    def update_lights(self):
        for light in self.lights:
            light.update_status()