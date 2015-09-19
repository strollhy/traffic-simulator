__author__ = 'hongyusong'

import random

from lane import Lane
from observer import Observable
f = open('data/density.txt', 'w')


class MainLink(Observable):
    def __init__(self, *data):
        super(MainLink, self).__init__()
        self.link_id = data[0]
        self.length = float(data[1]) * 0.000189394 if data[1] else 200  # if no length is provided, assume infinite
        self.max_cap = int(self.length / 0.00279617)
        self.num_of_lanes = int(data[2])
        self.min_speed = int(data[3])
        self.max_speed = int(data[4])
        self.jam_density = int(data[5])
        self.time = 0

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

    def update_time(self, time):
        self.time = time

    def add_car(self, car):
        self.notify_observers("Car #%s reaches link #%s" % (car.car_id, self.link_id))
        # update car status
        car.update_path()
        car.update_arrive_time(self.time)

        # check car status
        if not car.get_destination():
            self.notify_observers("Car #%s reaches its destination" % car.car_id)
            return

        # assign lane group to car
        if not self.assign_lane_group(car):
            self.notify_observers("Car #%s reaches dead end, couldn't find a path from %s to %s" % (car.car_id, self.link_id, car.get_destination()))
            return

        # add to sublink1
        self.sublink1.add_car(car)

    def assign_lane_group(self, car):
        heading_link = car.get_destination()
        if self.left_link and self.left_link.link_id == heading_link:
            car.lane_group = 'L'
        elif self.right_link and self.right_link.link_id == heading_link:
            car.lane_group = 'R'
        elif self.through_link and self.through_link.link_id == heading_link:
            car.lane_group = 'T'
        else:
            return False
        return True

    def update_status(self):
        self.cal_velocity()

    def get_capacity(self):
        return self.max_cap - self.sublink2.get_car_num() - self.sublink3.get_car_num() - self.sublink1.get_car_num()

    def cal_density(self):
        x = self.sublink2.get_car_num() + self.sublink3.get_car_num()
        N = x + self.sublink1.get_car_num()
        n = self.num_of_lanes
        l = self.length
        rho_jam = 220.0
        rho = (N-x)/(n*l-x/rho_jam + .1)
        f = open('data/density.txt', 'a')
        f.write("%s,%d,%d,%d,%f,%f,%d,%d\n" % (self.link_id, N, x, n, l, rho, self.sublink2.pass_count, self.time))
        f.close()
        return rho

    def cal_velocity(self):
        if self.length == 0: return
        v_min = self.min_speed
        v_free = self.max_speed
        rho = self.cal_density()
        rho_jam = 220.0
        alpha = 1.2
        beta = 1.8
        self.avg_speed = v_min + (v_free - v_min) * (1-(rho/rho_jam)**alpha)**beta


class SubLink(object):
    def __init__(self, link, lane_num):
        self.link = link
        self.lanes = [[] for i in xrange(lane_num)]

    def get_car_num(self):
        return sum([len(l) for l in self.lanes])


class SubLink1(SubLink):
    def add_car(self, car):
        car.update_arrive_time(self.link.time)
        direction = car.lane_group
        if direction == "T":
            i = random.randint(0, len(self.lanes) - 1)
            self.lanes[i].append(car)
        elif direction == "R":
            self.lanes[-1].append(car)
        else:
            self.lanes[0].append(car)

    def release_cars(self):
        for i in xrange(len(self.lanes)):
            for car in self.lanes[i]:
                if self.link.sublink2.add_car(car, i):
                    self.lanes[i].remove(car)
                    car.update_arrive_time(self.link.time)


class SubLink2(SubLink):
    def __init__(self, link, lane_num):
        SubLink.__init__(self, link, lane_num)

        self.allowed_merge = {}
        self.allowed_merge["L"] = lane_num
        self.allowed_merge["R"] = lane_num
        self.allowed_merge["T"] = lane_num
        self.pass_count = 0

    def add_car(self, car, from_lane):
        # if car reaches the zone
        if self.in_zone(car):
            self.lanes[self.get_to_lane(from_lane)].append(car)
            car.update_arrive_time(self.link.time)
            return True
        else:
            return False

    def in_zone(self, car):
        car.distance += self.link.avg_speed * 10.0 / 3600
        if car.distance > self.get_abscissa() or self.link.length >= 200:
            car.distance = 0
            self.pass_count += 1
            return True
        else:
            return False

    def get_abscissa(self):
        return self.link.length - max([len(l) for l in self.lanes]) / self.link.jam_density

    def get_to_lane(self, from_number):
        return from_number

    def count_cars_in_lane_group(self, lane, direction):
        return len([c for c in lane if direction == c.lane_group])

    def cal_blockage_factor(self, direction):
        if direction == "L":
            # if totally blocked on the group
            # TODO make it blocked if related through lane is blocked
            if self.link.sublink3.empty_space(direction) == 0:
                return 1
            else:
                cnt_l = self.count_cars_in_lane_group(self.lanes[0], 'L')
                cnt_t = self.count_cars_in_lane_group(self.lanes[0], 'T')
                return cnt_t / (cnt_l + cnt_t + .1)

        elif direction == "R":
            # TODO make it blocked if related through lane is blocked
            if self.link.sublink3.empty_space(direction) == 0:
                return 1
            else:
                cnt_l = self.count_cars_in_lane_group(self.lanes[0], "L")
                cnt_t = self.count_cars_in_lane_group(self.lanes[0], "T")

                cnt_t_2 = self.count_cars_in_lane_group(self.lanes[-1], "T")
                cnt_r = self.count_cars_in_lane_group(self.lanes[-1], "R")
                return cnt_l / (cnt_t + cnt_l + .1) + cnt_r / (cnt_t_2 + cnt_r + .1)

        elif "T" in direction:
            if self.link.sublink3.empty_space(direction) == 0:
                return 1
            else:
                cnt_r = self.count_cars_in_lane_group(self.lanes[-1], 'R')
                cnt_t = self.count_cars_in_lane_group(self.lanes[-1], 'T')
                return cnt_t * 1.0 / (cnt_r + cnt_t + .1)

    def update_allowed_merge(self):
        for k in self.allowed_merge.keys():
            # hard coded for single lane
            if self.link.sublink3.single_lane:
                self.allowed_merge['T'] = 5
                self.allowed_merge['L'] = 3
                self.allowed_merge['R'] = 3
            else:
                blockage_factor = self.cal_blockage_factor(k)
                self.allowed_merge[k] = min(self.link.sublink3.empty_space(k),
                                            max(1 - blockage_factor, 0) * self.get_car_num())

    def release_cars(self):
        self.update_allowed_merge()

        moved_car = 1
        while moved_car != 0:
            moved_car = 0
            # pop on each lane
            for lane in self.lanes:
                if len(lane) > 0:
                    car = lane[0]
                    if not car.is_blocked:
                        lane_group = car.lane_group
                        # Bypassing unknown directions
                        if self.allowed_merge[lane_group] > 0 and self.link.sublink3.add_car(car):
                            lane.pop(0)
                            moved_car += 1
                            self.allowed_merge[car.lane_group] -= 1
                            self.link.notify_observers("Adding car #%s to waiting group %s, %s" % (car.car_id, car.lane_group, self.link.link_id + '->' + car.get_destination()))
                        else:
                            car.is_blocked = True
                            self.link.notify_observers("Car #%s is blocked on %s, %s" % (car.car_id, car.get_destination(), lane_group))

        for lane in self.lanes:
            for car in lane:
                car.is_blocked = False


class SubLink3(SubLink):
    def __init__(self, link, caps):
        self.link = link
        self.signals = {"T": [], "L": [], "R": []}
        self.lanes = []
        self.single_lane = False
        caps = [int(c) for c in caps]

        if sum(caps) == 5:
            self.single_lane = True
            self.lanes.append(Lane(link, self, 'LTR', max(caps)))
            return

        if caps[0] == 5:
            self.lanes.append(Lane(link, self, 'LT', caps[0]))
        else:
            self.lanes.append(Lane(link, self, 'L', caps[0]))

        if caps[-1] == 5:
            self.lanes.append(Lane(link, self, 'RT', caps[-1]))
        else:
            self.lanes.append(Lane(link, self, 'R', caps[-1]))

        for cap in caps[1:-1]:
            self.lanes.append(Lane(link, self, 'T', cap))

    def setup_signal(self, group, data):
        self.signals[group] = data

    def get_car_num(self):
        return sum(len(l.cars) for l in self.lanes)

    def empty_space(self, lane_group):
        s = 0
        lanes = sorted(self.lanes, key=lambda x: x.empty_space(), reverse=True)
        for lane in lanes:
            if lane_group in lane.type and lane.empty_space():
                s += lane.empty_space()
        return s

    def get_empty_lane(self, lane_group):
        lanes = sorted(self.lanes, key=lambda x: x.empty_space(), reverse=True)
        for lane in lanes:
            if lane_group in lane.type and lane.empty_space():
                return lane
            if self.single_lane and lane.empty_space():
                return lane
        return None

    def add_car(self, car):
        lane = self.get_empty_lane(car.lane_group)
        if lane:
            lane.add_car(car)
            car.is_blocked = False
            car.update_arrive_time(self.link.time)
            return True
        else:
            car.is_blocked = True
            self.link.notify_observers("Car #%s is blocked for waiting zone %s" % (car.car_id, car.lane_group))
            return False

    def release_cars(self):
        for lane in self.lanes:
            # TODO release a fixed number of cars each time
            while len(lane.cars) > 0 and lane.cars[0].is_blocked is False:
                car = lane.cars[0]
                direction = car.lane_group
                if direction == 'L' and (len(self.signals['L']) == 0 or self.signals['L'][self.link.time] == '1'):
                    if self.link.left_link:
                        if self.link.left_link.get_capacity():
                            self.link.notify_observers("Car #%s left turn to Link #%s" % (car.car_id, self.link.left_link.link_id))
                            lane.cars.pop(0)
                            self.link.left_link.add_car(car)
                        else:
                            car.is_blocked = True
                    else:
                        lane.cars.pop(0)
                    continue

                if direction == 'R' and (len(self.signals["R"]) == 0 or self.signals["R"][self.link.time] == '1'):
                    if self.link.right_link:
                        if self.link.right_link.get_capacity():
                            self.link.notify_observers("Car #%s right turn to Link #%s" % (car.car_id, self.link.right_link.link_id))
                            lane.cars.pop(0)
                            self.link.right_link.add_car(car)
                        else:
                            car.is_blocked = True
                    else:
                        lane.cars.pop(0)
                    continue

                if direction == 'T' and (len(self.signals["T"]) == 0 or self.signals["T"][self.link.time] == '1'):
                    if self.link.through_link:
                        if self.link.through_link.get_capacity():
                            self.link.notify_observers("Car #%s move to Link #%s" % (car.car_id, self.link.through_link.link_id))
                            self.link.through_link.add_car(car)
                            lane.cars.pop(0)
                        else:
                            car.is_blocked = True
                    else:
                        lane.cars.pop(0)
                    continue

                self.link.notify_observers("Car #%s is waiting on %s light to %s" % (car.car_id, car.lane_group, car.get_destination()))
                car.is_blocked = True

        # after release reset block flag
        for lane in self.lanes:
            for car in lane.cars:
                car.is_blocked = False