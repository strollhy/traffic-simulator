__author__ = 'hongyusong'


class Car():
    def __init__(self, car_id, start_time, path):
        self.car_id = car_id
        self.path = path.split("-")
        self.start_time = start_time
        self.distance = 0
        self.arrive_time = []
        self.step = -1
        self.direction = []
        self.is_blocked = False

    def get_directions(self, func):
        for i in xrange(1, len(self.path)):
            self.direction.append(func(self.path[i-1], self.path[i]))
        self.direction.append(None)

    def heading_direction(self):
        return self.direction[self.step]

    def update_status(self):
        self.step += 1
        if self.step == len(self.path) - 1:
            print "Car #%s has reached its destination." % self.car_id
            return False
        return True

class Lane:
    def __init__(self, link, sublink, type, capacity):
        self.link = link
        self.sublink = sublink
        self.type = type
        self.capacity = capacity
        self.cars = []

    def add_car(self, car):
        self.cars.append(car)

    def remove_car(self):
        return self.cars.pop(0)

    def empty_space(self):
        return self.capacity - len(self.cars)