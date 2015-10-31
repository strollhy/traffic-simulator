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

        self.next_link = {"T": None, "L": None, "R": None}
        self.conflict_link = None

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
        """
        Add car to the main link

        :param car:
        :return:
        """
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
        for group, link in self.next_link.items():
            if link and link.link_id == heading_link:
                car.lane_group = group
                return True
        return False

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

    def release_cars(self):
        self.sublink3.release_cars(5)
        self.sublink2.release_cars(5)
        self.sublink1.release_cars()

    def post_release(self):
        self.sublink3.post_release()


class SubLink(object):
    def __init__(self, link, lane_num):
        self.link = link
        self.lanes = [[] for _ in xrange(lane_num)]

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
        self.allowed_merge = {"L": lane_num, "R": lane_num, "T": lane_num}
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

    @staticmethod
    def get_to_lane(from_number):
        return from_number

    @staticmethod
    def count_cars_in_lane_group(lane, direction):
        return len([c for c in lane if direction == c.lane_group])

    def cal_blockage_factor(self, direction):
        if direction == "L":
            # if totally blocked on the group
            cnt_l = self.count_cars_in_lane_group(self.lanes[0], 'L')
            cnt_t = self.count_cars_in_lane_group(self.lanes[0], 'T')
            return cnt_t / (cnt_l + cnt_t + .1)

        elif direction == "R":
            cnt_l = self.count_cars_in_lane_group(self.lanes[0], "L")
            cnt_t = self.count_cars_in_lane_group(self.lanes[0], "T")

            cnt_t_2 = self.count_cars_in_lane_group(self.lanes[-1], "T")
            cnt_r = self.count_cars_in_lane_group(self.lanes[-1], "R")
            return cnt_l / (cnt_t + cnt_l + .1) + cnt_r / (cnt_t_2 + cnt_r + .1)

        elif "T" in direction:
            cnt_r = self.count_cars_in_lane_group(self.lanes[-1], 'R')
            cnt_t = self.count_cars_in_lane_group(self.lanes[-1], 'T')
            return cnt_t * 1.0 / (cnt_r + cnt_t + .1)

    def update_allowed_merge(self):
        for lane_group in self.allowed_merge.keys():
            # hard coded for single lane
            if self.link.sublink3.single_lane:
                self.allowed_merge['T'] = 5
                self.allowed_merge['L'] = 3
                self.allowed_merge['R'] = 3
            else:
                blockage_factor = self.cal_blockage_factor(lane_group)
                self.allowed_merge[lane_group] = max(1 - blockage_factor, 0) * self.get_car_num()

    def release_cars(self, car_per_line):
        """
        Try to release car from each lane to merging section

        :param car_per_line: int, the chances that each lane has to release the cars
        :return:
        """
        self.update_allowed_merge()
        for _ in xrange(car_per_line):
            waiting_queue = []

            for lane_number in xrange(len(self.lanes)):
                # skip if either lane is empty or first car is block
                if not self.lanes[lane_number] or self.lanes[lane_number][0].is_blocked:
                    continue

                lane = self.lanes[lane_number]
                car = lane[0]

                # if allow merged on this lane group and also find an empty space
                if self.allowed_merge[car.lane_group] > 0:
                    available_lane, potential_lanes = self.link.sublink3.find_available_lanes(car.lane_group, lane_number)
                    if available_lane:
                        # if there is a lane directly accessible, then release the car
                        self.__release_car_to_next(lane_number, available_lane[0])
                    elif potential_lanes:
                        # if there is a potential lane available, put the car to waiting list
                        waiting_queue.append([lane_number, potential_lanes])
                    else:
                        car.set_blocked("No space left on merging zone. %d" % (self.link.sublink3.group_capacity(car.lane_group)))
                else:
                    car.set_blocked("Merging not allowed.")

            # Provide one more chance to move car to potential lanes
            for elem in waiting_queue:
                for lane in elem[1]:
                    if lane.empty_space():
                        self.__release_car_to_next(elem[0], lane)
                        break

        # reset car status for next time stamp
        # TODO put this somewhere else
        for lane in self.lanes:
            for car in lane:
                car.unset_blocked()

    def __release_car_to_next(self, lane_number, next_lane):
        """
        Actual releasing part

        :param lane_number:
        :param next_lane:
        :return:
        """
        car = self.lanes[lane_number].pop(0)
        self.allowed_merge[car.lane_group] -= 1
        self.link.sublink3.add_car(car, next_lane)
        self.link.notify_observers("Adding car #%s to merging group %s, %s"
                                   % (car.car_id, car.lane_group, self.link.link_id + '->' + car.get_destination()))


class SubLink3(SubLink):
    def __init__(self, link, capacities):
        self.link = link
        self.signals = {"T": [], "L": [], "R": []}
        self.lanes = {"T": [], "L": [], "R": []}
        self.single_lane = False
        self.car_num = 0
        self.capacity = 0
        self.released = False   # indicate whether released or not for this timestamp
        self.init_lanes(capacities)

    def get_car_num(self):
        return self.car_num

    def setup_signal(self, group, data):
        self.signals[group] = data

    def init_lanes(self, capacities):
        """
        Initialize lanes for each lane group, different lane groups might share the same lane

        :param capacities:
        :return:
        """
        capacities = [int(c) for c in capacities]
        self.capacity = sum(capacities)
        if sum(capacities) == 5:
            # if it's single lane, then all group share the same lane
            self.single_lane = True
            lane = Lane(self.link, self, max(capacities))
            self.lanes["T"].append(lane)
            self.lanes["L"].append(lane)
            self.lanes["R"].append(lane)
        else:
            # create left,right lanes
            left_lane = Lane(self.link, self, capacities[0])
            right_lane = Lane(self.link, self, capacities[-1])
            self.lanes["L"].append(left_lane)
            self.lanes["R"].append(right_lane)

            # create through lanes
            for cap in capacities[1:-1]:
                if cap:
                    self.lanes["T"].append(Lane(self.link, self, cap))

            # if capacity is 5, then left/right and through group share the same lane
            if capacities[0] == 5:
                self.lanes["T"].insert(0, left_lane)
            if capacities[-1] == 5:
                self.lanes["T"].append(right_lane)

    def group_capacity(self, group):
        return sum([lane.empty_space() for lane in self.lanes[group]])

    def find_available_lanes(self, group, lane_number):
        """
        Find empty space for given lane group

        :param group: string, lane group the car belongs to
        :param lane_number: int, lane number the car is at
        :return: list of Lane
        """
        available_lanes = []      # lanes that can be merged to directly
        potential_lanes = []      # lanes that need to wait on other cars

        if group == "T":
            # find empty spot at front and near the lane
            # if lane is merging, pick the nearest lane as primary lane
            lane_number = min(lane_number, len(self.lanes[group]) - 1)
            available_lanes.append(self.lanes[group][lane_number])

            # find secondary lanes, in case primary lane is full
            if 0 < lane_number:
                potential_lanes.append(self.lanes[group][lane_number-1])
            if lane_number < len(self.lanes[group]) - 1:
                potential_lanes.append(self.lanes[group][lane_number+1])
        else:
            available_lanes = self.lanes[group]

        return [lane for lane in available_lanes if lane.empty_space()], \
               [lane for lane in potential_lanes if lane.empty_space()]

    def add_car(self, car, lane):
        """
        Add car to the lane, update status

        :param car:
        :param lane:
        :return:
        """
        lane.add_car(car)
        car.update_arrive_time(self.link.time)
        self.car_num += 1

    def remove_car(self, lane_group, lane_number):
        self.lanes[lane_group][lane_number].cars.pop(0)
        self.car_num -= 1

    def release_cars(self, cars_per_lane):
        """
        Release cars to next link

        :param cars_per_lane: allowed car numbers can be released each time
        :return:
        """
        # skip if already released
        if self.released:
            return

        # for left lane group
        self.release_left_group(cars_per_lane)
        for _ in xrange(cars_per_lane):
            self.release_through_group()
            self.release_right_group()

    def is_red_light(self, lane_group):
        return not (len(self.signals[lane_group]) == 0 or self.signals[lane_group][self.link.time] == '1')

    def release_left_group(self, cars_per_lane):
        # skip on read light or no left link exists
        if self.is_red_light("L"):
            return

        conflict_link = self.link.conflict_link
        if not conflict_link:
            for _ in xrange(cars_per_lane):
                self.release_group("L")
            return

        for _ in xrange(cars_per_lane):
            # predict collision
            # TODO assuming only conflict on through & left
            conflict_lane = conflict_link.sublink3.lanes["L"][0].cars
            current_lane = self.lanes["L"][0].cars

            if not conflict_lane:
                self.release_group("L")
            elif not current_lane:
                conflict_link.sublink3.release_group("L")
            else:
                # if both have cars, need to predict conflict
                car1, car2 = current_lane[0], conflict_lane[0]
                if self.has_conflict(car1, conflict_lane):
                    # if car 1 is blocked, then just release car 2
                    conflict_link.sublink3.release_car(car2, "L", 0)
                else:
                    if not self.has_conflict(car2, current_lane):
                        conflict_link.sublink3.release_car(car2, "L", 0)
                    self.release_car(car1, "L", 0)

    def has_conflict(self, car, conflict_lane):
        if car.lane_group == "L":
            for i, conflict_car in enumerate(conflict_lane):
                if conflict_car.lane_group == "T":
                    if self.predict_conflict(i):
                        self.link.notify_observers("Car #%s waits for Car #%s to move" % (car.car_id, conflict_car.car_id))
                        return True
                    else:
                        return False
        return False

    def predict_conflict(self, i):
        # TODO confirm coefficient here
        pT, pL = 1.6, 2.4
        coefficients = [2.98, 2.59, 2.13, 1.91, 1.86, 1.65]
        i = min(i, len(coefficients) - 1)

        return coefficients[i] + pT / 2 < pL / 2

    def release_car(self, car, lane_group, lane_number):
        if self.link.next_link[car.lane_group].get_capacity() > 0:
            self.link.notify_observers("Car #%s %s turn to Link #%s" %
                                       (car.car_id, car.lane_group, self.link.next_link[car.lane_group].link_id))
            self.remove_car(lane_group, lane_number)
            self.link.next_link[car.lane_group].add_car(car)
        else:
            car.set_blocked("No space left on next link")

    def release_through_group(self):
        self.release_group("T")

    def release_right_group(self):
        self.release_group("R")

    def release_group(self, lane_group):
        if self.is_red_light(lane_group):
            # skip if red light
            return

        # try to release cars
        for lane_number in xrange(len(self.lanes[lane_group])):
            lane = self.lanes[lane_group][lane_number]

            if not lane.cars or lane.cars[0].is_blocked:
                continue

            car = lane.cars[0]
            if self.link.next_link[car.lane_group].get_capacity() > 0:
                self.link.notify_observers("Car #%s %s turn to Link #%s" %
                                           (car.car_id, car.lane_group, self.link.next_link[car.lane_group].link_id))
                self.remove_car(lane_group, lane_number)
                self.link.next_link[car.lane_group].add_car(car)
            else:
                car.set_blocked("No space left on next link")

        # after release reset block flag
        for lane in self.lanes[lane_group]:
            for car in lane.cars:
                car.unset_blocked()

    def group_cars(self):
        """
        Group cars to seven types
        :return: array of types count
        """
        # seven types
        types = [0 for _ in xrange(7)]

        # For left lane group
        for lane in self.lanes["L"]:
            index = 0

            # type I
            while index < len(lane.cars):
                if lane.cars[index].lane_group == "T":
                    types[0] += 1
                else:
                    break
                index += 1

            # type II
            while index < len(lane.cars):
                if lane.cars[index].lane_group == "L":
                    types[1] += 1
                else:
                    break
                index += 1

            # type III
            types[2] = len(lane.cars[index:])

        # For right lane group
        for lane in self.lanes["R"]:
            index = 0

            # type I
            while index < len(lane.cars):
                if lane.cars[index].lane_group == "T":
                    types[3] += 1
                else:
                    break
                index += 1

            # type II
            while index < len(lane.cars):
                if lane.cars[index].lane_group == "R":
                    types[4] += 1
                else:
                    break
                index += 1

            # type III
            types[5] = len(lane.cars[index:])

        # For through lane group
        for lane in self.lanes["T"]:
            types[6] += len(lane.cars)

        return types

    def post_release(self):
        self.released = False