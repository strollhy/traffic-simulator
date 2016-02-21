from lane import Lane
from time import Time
from sublink import SubLink


class SubLink3(SubLink):
    def __init__(self, link, capacities):
        self.link = link
        self.signals = {"T": [], "L": [], "R": []}
        self.lanes = {"T": [], "L": [], "R": []}
        self.single_lane = False
        self.car_num = 0
        self.capacity = 0
        self.released = False   # indicate whether released or not for this time stamp
        self.init_lanes(capacities)

        self.pT, self.pL = 1.6, 2.4
        self.headway = [2.98, 2.59, 2.13, 1.91, 1.86, 1.65]
        self.pedestrian_time = 2

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

    def add_car(self, car, lane):
        lane.add_car(car)
        self.car_num += 1

    def find_available_lanes(self, group, lane_number):
        """
        Find empty space for given lane group

        :param group: string, lane group the car belongs to
        :param lane_number: int, lane number the car is at
        :return: list of Lane
        """
        available_lanes = []      # lanes that can be merged to directly

        if group == "T":
            available_lanes = sorted([lane for lane in self.lanes[group] if lane.empty_space()],
                                     key=lambda x: x.empty_space(),
                                     reverse=True)
        else:
            available_lanes = [lane for lane in self.lanes[group] if lane.empty_space()]
        return available_lanes

    def remove_car(self, lane_group, lane_number):
        self.lanes[lane_group][lane_number].cars.pop(0)
        self.car_num -= 1

    def is_red_light(self, lane_group):
        return not (len(self.signals[lane_group]) == 0 or self.signals[lane_group][Time().time] == '1')

    def release_cars(self):
        # skip if already released
        if not self.released:
            self.release_left_group()
        self.release_group("T")
        self.release_group("R")

    def release_group(self, lane_group):
        if self.is_red_light(lane_group):
            # skip if red light
            for lane in self.lanes[lane_group]:
                lane.elapsed_time = 0
            return

        # try to release cars
        for lane_number, lane in enumerate(self.lanes[lane_group]):
            car_cnt = 0
            while lane.cars and not lane.cars[0].is_blocked and lane.elapsed_time <= 10 - self.headway[-1]:
                # consider pedestrian
                if lane.cars[0].lane_group == "R":
                    if car_cnt == 0:
                        lane.elapsed_time += self.pedestrian_time
                    else:
                        car_cnt += 1

                self.release_car(lane.cars[0], lane_group, lane_number)
                lane.elapsed_time += self.headway[-1]

            if lane.elapsed_time > 10 - self.headway[-1]:
                lane.elapsed_time -= self.headway[-1]

        # after release reset block flag
        for lane in self.lanes[lane_group]:
            for car in lane.cars:
                car.unset_blocked()

    def release_left_group(self):
        current_lane = self.lanes["L"][0]
        conflict_link = self.link.conflict_link

        # TODO check on which light?
        skip_current = self.is_red_light("L")
        skip_conflict = not conflict_link or conflict_link.sublink3.is_red_light("L")

        if skip_current and skip_conflict:
            for lane in self.lanes["L"]:
                lane.elapsed_time = 0

            if conflict_link:
                for lane in self.lanes["L"]:
                    lane.elapsed_time = 0
        elif skip_current:
            conflict_link.sublink3.release_group("L")
        elif skip_conflict:
            self.release_group("L")
        else:
            conflict_lane = conflict_link.sublink3.lanes["L"][0]

            while current_lane.elapsed_time <= 10 - self.headway[-1] and \
                    conflict_lane.elapsed_time <= 10 - self.headway[-1]:
                # predict collision
                # if both have cars, need to predict conflict
                if not current_lane.cars or current_lane.elapsed_time > 10 - self.headway[-1]:
                    conflict_link.sublink3.release_group("L")
                    break
                elif not conflict_lane.cars or conflict_lane.elapsed_time > 10 - self.headway[-1]:
                    self.release_group("L")
                    break
                else:
                    car1, car2 = current_lane.cars[0], conflict_lane.cars[0]
                    has_conflict, release_time = self.get_conflict(car1, conflict_lane)
                    if has_conflict or car1.is_blocked:
                        # if car 1 is blocked, then just release car 2
                        conflict_link.sublink3.release_car(car2, "L", 0)
                        current_lane.elapsed_time += release_time
                        conflict_lane.elapsed_time += release_time
                    else:
                        self.release_car(car1, "L", 0)
                        current_lane.elapsed_time += release_time
                        conflict_lane.elapsed_time += release_time

                print current_lane.elapsed_time, conflict_lane.elapsed_time

        # Mark as visited
        # TODO can we simplify this?
        self.released = True
        if conflict_link:
            conflict_link.released = True

    def get_conflict(self, car, conflict_lane):
        release_time = self.pL if car.lane_group == "L" else self.pT
        if car.lane_group == "L":
            for i, conflict_car in enumerate(conflict_lane.cars):
                if conflict_car.lane_group == "T":
                    through_time = sum(self.headway[1:i+1])
                    if through_time + self.pT / 2 < self.pL / 2:
                        self.link.notify_observers("Car #%s waits for Car #%s to move" % (car.car_id, conflict_car.car_id))
                        return True, through_time
                    else:
                        return False, release_time
        return False, release_time

    def release_car(self, car, lane_group, lane_number):
        if self.link.next_link[car.lane_group].get_capacity() > 0:
            self.link.notify_observers("Car #%s %s turn to Link #%s" %
                                       (car.car_id, car.lane_group, self.link.next_link[car.lane_group].link_id))
            self.remove_car(lane_group, lane_number)
            self.link.next_link[car.lane_group].add_car(car)
        else:
            car.set_blocked("No space left on next link")

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