from util.observer import Observable
from time import Time
# TODO f = open('data/density.txt', 'w')


class Link(Observable):
    def __init__(self):
        super(Link, self).__init__()

        self.link_id = None
        self.normalized_id = None
        self.length = None
        self.lanes_num = None
        self.max_cap = None
        self.next_link = {"T": None, "L": None, "R": None}
        self.conflict_link = None
        self.sublink1 = self.sublink2 = self.sublink3 = None
        self.type = None

        self.relative_time = 0
        self.min_speed = 5
        self.max_speed = 45
        self.jam_density = 220
        self.num_of_cars = 0
        self.avg_speed = 0

    def __repr__(self):
        return "#%s(%s) %s [l:%s] %s" % (self.link_id, self.normalized_id, self.type, self.length, self.__cap__())

    def __cap__(self):
        return "[cap: %d %d %d %d]" % (self.capacity, self.sublink1.car_num, self.sublink2.car_num, self.sublink3.car_num)

    @property
    def capacity(self):
        return self.max_cap - self.sublink1.car_num - self.sublink2.car_num - self.sublink3.car_num

    def add_car(self, car):
        # TODO won't allow car in if link is jamed
        self.notify_observers("Car %s reaches link %s" % (car, self))

        if self.car_can_proceed(car):
            #TODO fix car.od
            if car.od in self.simulator.paths and car.path_id in self.simulator.paths[car.od]:
                self.simulator.paths[car.od][car.path_id].elapse_time += car.arrive_time - car.start_time
            # print car.path_id, car.arrive_time - car.start_time
            # print self.simulator.paths[car.od][car.path_id].elapse_time

            self.sublink1.add_car(car)

    def car_can_proceed(self, car):
        if car.reach_destination() or not self.assign_lane_group(car):
            return False
        else:
            return True

    def assign_lane_group(self, car):
        heading_link = car.next_link
        if heading_link:
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
        x = self.sublink2.car_num + self.sublink3.car_num
        N = x + self.sublink1.car_num
        n = self.lanes_num
        l = self.length
        rho = (N-x)/(n*l-x/self.jam_density + .1)
        return rho

    def release_cars(self):
        self.sublink1.release_cars()
        if self.conflict_link:
            self.conflict_link.sublink1.release_cars()

        self.relative_time = 0
        while self.relative_time < Time().time_stamp:
            tao = min([len(lane.cars) for lane in self.sublink3.lanes]) * 1.5
            tao = min(tao, min([len(lane.cars) for lane in self.conflict_link.sublink3.lanes])) if self.conflict_link else tao
            tao = max(tao, 1.5)
            self.sublink2.release_cars()
            self.sublink3.release_cars(tao)
            self.relative_time += tao

    def post_release(self):
        pass
        # self.sublink3.post_release()