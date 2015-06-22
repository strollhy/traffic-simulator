__author__ = 'hongyusong'


class Car():
    def __init__(self, car_id, path, start_time):
        self.car_id = car_id
        self.path = path.split(",")
        self.start_time = start_time
        self.distance = 0
        self.arrive_time = []
        self.step = 1

    def get_next_link_id(self):
        return self.path[self.step]

    def update_status(self):
        self.step += 1
        if self.step == len(self.path):
            print "Car #%s has reached the destination." % self.car_id


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


class Link(object):
    def __init__(self):
        pass


class MainLink(Link):
    def __init__(self, link_id, length, num_of_lanes, min_speed,
                 max_speed, jam_density, left_cap, right_cap, through_cap):
        self.link_id = link_id
        self.length = length
        self.num_of_lanes = num_of_lanes
        self.max_speed = min_speed
        self.min_speed = max_speed
        self.jam_density = jam_density

        self.left_link = None
        self.right_link = None
        self.through_link = None

        self.num_of_cars = 0
        self.capacity = 0
        self.avg_speed = 0
        self.sublink1 = SubLink1(self)
        self.sublink2 = SubLink2(self)
        self.sublink3 = SubLink3(self)
        self.sublink3.left_cap = left_cap
        self.sublink3.right_cap = right_cap
        self.sublink3.through_cap = through_cap

    def add_car(self, car):
        self.sublink1.add_car(car)

    def update_status(self):
        pass

    def get_direction(self, next_link_id):
        if self.left_link and self.left_link.link_id == next_link_id:
            return "left"
        if self.right_link and self.right_link.link_id == next_link_id:
            return "right"
        if self.through_link and self.through_link.link_id == next_link_id:
            return "through"

    def print_status(self):
        pass


class SubLink(Link):
    def __init__(self, link):
        self.link = link
        self.cars = []


class SubLink1(SubLink):
    def add_car(self, car):
        self.cars.append(car)

    def update_cars(self):
        for car in self.cars:
            if self.link.sublink2.add_car(car):
                self.cars.remove(car)


class SubLink2(SubLink):
    def __init__(self, link):
        super(SubLink2, self).__init__(link)

    def add_car(self, car):
        self.cars.append(car)
        return True

    def update_cars(self):
        for car in self.cars:
            if self.link.sublink3.add_car(car):
                self.cars.remove(car)


class SubLink3(SubLink):
    def __init__(self, link):
        super(self.__class__, self).__init__(link)
        self.lights = []
        self.left_lane = [] #cars in the last left lane
        self.right_lane = [] #cars in the last right lane
        self.through_lane = [] #cars in the last through lane
        self.left_cap = 0
        self.right_cap = 0
        self.through_cap = 0

    def add_car(self, car):
        next_link_id = car.get_next_link_id()
        direction = self.link.get_direction(next_link_id)

        if direction == 'left':
            if len(self.left_lane) < self.left_cap:
                self.left_lane.append(car)
                return True

        elif direction == 'through':
            if len(self.through_lane) < self.through_cap:
                self.through_lane.append(car)
                return True

        elif direction == 'right':
            if len(self.right_lane) < self.right_cap:
                self.right_lane.append(car)
                return True

        return False

    def update_cars(self):
        if self.lights[0] and self.link.left_link:
            while len(self.left_lane) > 0:
                car = self.left_lane.pop(0)
                print "Car #%s left turn to Link #%s" % (car.car_id, self.link.left_link.link_id)
                self.link.left_link.add_car(car)
                car.update_status()

        if self.lights[1] and self.link.through_link:
            while len(self.through_lane) > 0:
                car = self.through_lane.pop(0)
                print "Car #%s moving to Link #%s" % (car.car_id, self.link.through_link.link_id)
                self.link.through_link.add_car(car)
                car.update_status()

        if self.lights[2] and self.link.right_link:
            while len(self.right_lane) > 0:
                car = self.right_lane.pop(0)
                print "Car #%s right turn to Link #%s" % (car.car_id, self.link.right_link.link_id)
                self.link.right_link.add_car(car)
                car.update_status()

    def update_lights(self, time):
        for light in self.lights:
            light.update_status(time)

    def get_lights(self):
        return ",".join([str(light.light) for light in self.lights])

    def print_lights(self):
        print "Link #%s::" % self.link.link_id + self.get_lights()