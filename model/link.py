from util.observer import Observable
from time import Time
# TODO f = open('data/density.txt', 'w')


class Link(Observable):
    def __init__(self, *data):
        super(Link, self).__init__()

        self.link_id = None
        self.length = None
        self.num_of_lanes = None
        self.min_speed = None
        self.max_speed = None
        self.max_cap = None
        self.jam_density = None
        self.next_link = {"T": None, "L": None, "R": None}
        self.conflict_link = None
        self.sublink1 = self.sublink2 = self.sublink3 = None

        self.num_of_cars = 0
        self.avg_speed = 0

    def __repr__(self):
        return "#%s [capacity: %d]" % (self.link_id, self.capacity)

    @property
    def capacity(self):
        return self.max_cap - self.sublink2.get_car_num() - self.sublink3.get_car_num() - self.sublink1.get_car_num()

    def add_car(self, car):
        # TODO won't allow car in if link is jamed
        self.notify_observers("Car %s reaches link %s" % (car, self))

        if self.car_can_proceed(car):
            self.sublink1.add_car(car)

    def car_can_proceed(self, car):
        car.move_on()

        if car.reach_destination() or not self.assign_lane_group(car):
            return False
        else:
            return True

    def assign_lane_group(self, car):
        heading_link = car.next_link
        for group, link in self.next_link.items():
            if link and link.link_id == heading_link:
                car.lane_group = group
                return True
        self.notify_observers("Car %s reaches dead end, couldn't find a path" % car)
        return False

    def update_status(self):
        self.calculate_velocity()

    def calculate_velocity(self):
        if self.length == 0: return
        v_min = self.min_speed
        v_free = self.max_speed
        rho = self.calculate_density()
        rho_jam = 220.0
        alpha = 1.2
        beta = 1.8
        self.avg_speed = v_min + (v_free - v_min) * (1-(rho/rho_jam)**alpha)**beta

    def calculate_density(self):
        x = self.sublink2.get_car_num() + self.sublink3.get_car_num()
        N = x + self.sublink1.get_car_num()
        n = self.num_of_lanes
        l = self.length
        rho = (N-x)/(n*l-x/self.jam_density + .1)
        return rho

    def release_cars(self):
        self.sublink1.release_cars()
        self.sublink2.release_cars(10)
        self.sublink3.release_cars()

    def post_release(self):
        self.sublink3.post_release()