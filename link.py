__author__ = 'hongyusong'

import random
from traffic import Lane


class MainLink():
    def __init__(self, *data):
        self.link_id = data[0]
        self.length = float(data[1]) if data[1] else 0
        self.num_of_lanes = int(data[2])
        self.max_speed = int(data[3])
        self.min_speed = int(data[4])
        self.jam_density = int(data[5])

        self.left_link = None
        self.right_link = None
        self.through_link = None

        self.num_of_cars = 0
        self.capacity = 0
        self.avg_speed = 0
        self.lane_num = len(data[6:]) - 1
        self.sublink1 = SubLink1(self, self.lane_num)
        self.sublink2 = SubLink2(self, self.lane_num)
        self.sublink3 = SubLink3(self, data[6:])

    def add_car(self, car):
        self.sublink1.add_car(car)

    def update_status(self):
        self.cal_velocity()

    def cal_density(self):
        x = self.sublink1.get_car_num() + self.sublink2.get_car_num()
        N = x + self.sublink3.get_car_num()
        n = self.num_of_lanes
        l = self.length
        rho_jam = 220.0
        # TODO double check that N-x is really counting sublink 3
        rho = (N-x)/(n*l-x/rho_jam + .1)
        return rho

    def cal_velocity(self):
        v_min = self.min_speed
        v_free = self.max_speed
        rho = self.cal_density()
        rho_jam = 220.0
        alpha = 1.2
        beta = 1.8
        self.avg_speed = v_min + (v_min+v_free) * (1-(rho/rho_jam)**alpha)**beta

    def print_status(self):
        pass


class SubLink(object):
    def __init__(self, link, lane_num):
        self.link = link
        self.lanes = [[] for i in xrange(lane_num)]

    def get_car_num(self):
        return sum([len(l) for l in self.lanes])


class SubLink1(SubLink):
    def add_car(self, car):
        if car.update_status() is False:
            return

        direction = car.heading_direction()
        if direction == "T":
            i = random.randint(1, len(self.lanes) - 1)
            self.lanes[i].append(car)
        elif direction == "R":
            self.lanes[-1].append(car)
        else:
            self.lanes[0].append(car)

    def update_cars(self):
        for i in xrange(len(self.lanes)):
            for car in self.lanes[i]:
                if self.link.sublink2.add_car(car, i):
                    self.lanes[i].remove(car)


class SubLink2(SubLink):
    def __init__(self, link, lane_num):
        super(SubLink2, self).__init__(link, lane_num)
        self.allowed_merge = {}
        self.allowed_merge["L"] = lane_num
        self.allowed_merge["R"] = lane_num
        self.allowed_merge["T"] = lane_num

    def add_car(self, car, from_lane):
        # if car reaches
        if self.in_zone(car):
            self.lanes[self.get_to_lane(from_lane)].append(car)
            return True
        else:
            return False

    def in_zone(self, car):
        car.distance += self.link.avg_speed
        if car.distance > self.get_abscissa():
            car.distance = 0
            return True
        else:
            return False

    def get_abscissa(self):
        return self.link.length - max([len(l) for l in self.lanes]) / self.link.jam_density

    def get_to_lane(self, from_number):
        return from_number

    def count_cars(self, lane, direction):
        return len([c for c in lane if direction in c.direction])

    def cal_blockage_factor(self, direction):
        if direction == "L":
            # if totally block on the group
            if self.link.sublink3.empty_space(direction) == 0 or self.link.sublink3.lanes[1].empty_space() == 0:
                return 1
            else:
                cnt_l = self.count_cars(self.lanes[0], 'L')
                cnt_t = self.count_cars(self.lanes[0], 'T')
                return cnt_t / (cnt_l + cnt_t + .1)

        elif direction == "R":
            if self.link.sublink3.empty_space(direction) == 0:
                return 1
            else:
                cnt_l = self.count_cars(self.lanes[0], "L")
                cnt_t = self.count_cars(self.lanes[0], "T")

                cnt_t_2 = self.count_cars(self.lanes[-1], "T")
                cnt_r = self.count_cars(self.lanes[-1], "R")
                return cnt_l / (cnt_t + cnt_l + .1) + cnt_r / (cnt_t_2 + cnt_r + .1)
        elif "T" in direction:
            if self.link.sublink3.empty_space(direction) == 0 or self.link.sublink3.lanes[-2].empty_space() == 0:
                return 1
            else:
                cnt_r = self.count_cars(self.lanes[-1], 'R')
                cnt_t = self.count_cars(self.lanes[-1], 'T')
                return cnt_t * 1.0 / (cnt_r + cnt_t + .1)

    def update_allowed_merge(self):
        for k in self.allowed_merge.keys():
            if self.lanes[0].type == "LTR":
                blockage_factor = 0
            else:
                blockage_factor = self.cal_blockage_factor(k)
            self.allowed_merge[k] = min(self.link.sublink3.empty_space(k),
                                        max(1 - blockage_factor, 0) * self.get_car_num())

    def update_cars(self):
        self.update_allowed_merge()

        while True:
            moved_car = 0
            for lane in self.lanes:
                if len(lane) > 0:
                    car = lane[0]
                    if car.is_blocked is False:
                        if self.allowed_merge[car.heading_direction()] > 0 and self.link.sublink3.add_car(car):
                            lane.pop(0)
                            moved_car += 1
                            self.allowed_merge[car.heading_direction()] -= 1
                            print "Adding car #%s to waiting group %s" % (car.car_id, car.heading_direction())
                        else:
                            car.is_blocked = True
                            print "Car #%s is blocked moving to %s" % (car.car_id, car.heading_direction())
            if moved_car == 0:
                break

        for lane in self.lanes:
            for car in lane:
                car.is_blocked = False


class SubLink3(SubLink):
    def __init__(self, link, caps):
        self.link = link
        self.signals = {"T": [], "L": [], "R": []}
        self.time = 0
        self.lanes = []
        caps = [int(c) for c in caps]

        if sum(caps) == 5:
            self.lanes.append(Lane(link, self, 'LTR', max(caps)))
            return

        if caps[0] == "5":
            self.lanes.append(Lane(link, self, 'LT', caps[0]))
        else:
            self.lanes.append(Lane(link, self, 'L', caps[0]))

        if caps[-1] == "5":
            self.lanes.append(Lane(link, self, 'RT', caps[-1]))
        else:
            self.lanes.append(Lane(link, self, 'R', caps[-1]))

        for cap in caps[1:-1]:
            self.lanes.append(Lane(link, self, 'T', cap))

    def setup_signal(self, group, data):
        self.signals[group] = data

    def get_car_num(self):
        return sum(len(l.cars) for l in self.lanes)

    def empty_space(self, heading_direction):
        s = 0
        lanes = sorted(self.lanes, key=lambda x: x.empty_space(), reverse=True)
        for lane in lanes:
            if heading_direction in lane.type and lane.empty_space():
                s += lane.empty_space()
        return s

    def get_empty_lane(self, heading_direction):
        lanes = sorted(self.lanes, key=lambda x: x.empty_space(), reverse=True)
        for lane in lanes:
            if heading_direction in lane.type and lane.empty_space():
                return lane
        return None

    def add_car(self, car):
        lane = self.get_empty_lane(car.heading_direction())
        if lane:
            lane.add_car(car)
            car.is_blocked = False
            return True
        else:
            car.is_blocked = True
            print "Car #%s is blocked for waiting zone %s" % (car.car_id, car.heading_direction())
            return False

    def update_cars(self):
        for lane in self.lanes:
            # TODO release a fixed number of cars each time
            if "L" in lane.type and len(self.signals['L']) and self.signals['L'][self.time]:
                while len(lane.cars) > 0:
                    car = lane.cars.pop(0)
                    print "Car #%s left turn to Link #%s" % (car.car_id, self.link.left_link.link_id)
                    self.link.left_link.add_car(car)

            if "R" in lane.type and len(self.signals["R"]) and self.signals["R"][self.time]:
                while len(lane.cars) > 0:
                    car = lane.cars.pop(0)
                    print "Car #%s right turn to Link #%s" % (car.car_id, self.link.right_link.link_id)
                    self.link.right_link.add_car(car)

            if "T" in lane.type and len(self.signals["T"]) and self.signals["T"][self.time]:
                while len(lane.cars) > 0:
                    car = lane.cars.pop(0)
                    print "Car #%s move to Link #%s" % (car.car_id, self.link.through_link.link_id)
                    self.link.through_link.add_car(car)

    def update_time(self, time):
        self.time = time