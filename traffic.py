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
        self.red_period = int(red_period)
        self.green_period = int(green_period)
        self.light = light

    def clone(self):
        return Light(self.red_period, self.green_period, self.light)

    def reverse_clone(self):
        return Light(self.green_period, self.red_period, 1 - self.light)

    def update_status(self, time):
        if self.light:
            if self.green_period <= time:
                self.light = 0
        else:
            if self.red_period <= time:
                self.light = 1


class Link():
    def __init__(self, link_id, length, num_of_lanes, min_speed,
                 max_speed, jam_density, left_cap, right_cap, through_cap):
        self.link_id = link_id
        self.length = length
        self.num_of_lanes = num_of_lanes
        self.max_speed = min_speed
        self.min_speed = max_speed
        self.jam_density = jam_density
        self.left_cap = left_cap
        self.right_cap = right_cap
        self.through_cap = through_cap

        self.num_of_cars = 0
        self.capacity = 0
        self.avg_speed = 0
        self.sublink_1 = [] #Cars in Sublink1
        self.sublink_2 = [] #Cars in Sublink2
        self.left_lane = [] #cars in the last left lane
        self.right_lane = [] #cars in the last right lane
        self.through_lane = [] #cars in the last through lane
        self.lights = []

    def update_lights(self, time):
        for light in self.lights:
            light.update_status(time)

    def get_lights(self):
        return ",".join([str(light.light) for light in self.lights])

    def print_lights(self):
        print "Link #%s::" % self.link_id + self.get_lights()