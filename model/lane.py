__author__ = 'hongyusong'


class Lane:
    def __init__(self, link, sublink, capacity):
        self.link = link
        self.sublink = sublink
        self.capacity = capacity
        self.headway_indx = 0
        self.elapsed_time = 0
        self.cars = []

    def add_car(self, car):
        self.cars.append(car)

    def remove_car(self):
        return self.cars.pop(0)

    def empty_space(self):
        return self.capacity - len(self.cars)