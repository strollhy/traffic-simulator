__author__ = 'hongyusong'


class Lane:
    def __init__(self, capacity):
        self.capacity = capacity
        self.overshoot_time = 0
        self.type = None
        self.link = None
        self.signal = None
        self.first_right = True
        self.cars = []

        self.headway_indx = 0
        self.pT, self.pL = 0.8, 1.2
        # self.headway = [1.65, 3.51, 5.42, 7.55, 10.14, 13.12]
        self.headway = [1.65, 1.86, 1.91, 2.13, 2.59, 2.98]
        self.pedestrian_time = 2

    def __repr__(self):
        return "<Type:%s Cap:%d Cars:%s>" % (self.type, self.empty_space, self.cars)

    @property
    def car_num(self):
        return len(self.cars)

    @property
    def empty_space(self):
        return self.capacity - self.car_num

    @property
    def conflict_lanes(self):
        if hasattr(self, "_conflict_lanes"):
            return self._conflict_lanes
        else:
            self._conflict_lanes = []
            if self.link.conflict_link:
                for lane in self.link.conflict_link.sublink3.lanes:
                    if "T" in lane.type:
                        self._conflict_lanes.append(lane)
            return self._conflict_lanes

    @property
    def is_green(self):
        return self.signal.is_green(self.link.relative_time)

    def can_release(self):
        return self.is_green and self.car_num # TODO and self.link.next_link[self.cars[0].lane_group].capacity > 0

    def add_car(self, car):
        self.cars.append(car)

    def remove_car(self):
        return self.cars.pop()

    def release_cars(self, granted_time):
        if self.can_release():
            self.granted_time = granted_time
            self.granted_time += self.overshoot_time
            while self.granted_time > 0:
                self.granted_time -= self._release_cars()
            self.overshoot_time = self.granted_time
        else:
            self.granted_time = 0
            self.headway_indx = 0
            self.overshoot_time = 0

    def _release_cars(self):
        car = self.cars[0]
        used_time = 0
        if car.lane_group == "L":
            used_time += self._release_left_group(car)
        elif car.lane_group == "T":
            used_time += self._release_through_group(car)
        else:
            used_time += self._release_right_group(car)
        return used_time

    def _release_car(self, car):
        car = self.cars.pop()
        car.move_on()

        self.link.next_link[car.lane_group].add_car(car)
        self.headway_indx += 1
        return self.headway[min(self.headway_indx - 1, len(self.headway)-1)]

    def release_time(self, car):
        # TODO normal release time plus headway
        return self.headway[0]

    def _release_left_group(self, car):
        conflict_lanes = self.conflict_lanes
        used_time = 0
        if not conflict_lanes:
            used_time += self._release_car(car)
        else:
            conflict_release_time = [0]
            for conflict_lane in conflict_lanes:
                if not conflict_lane.can_release():
                    continue

                conflict_car = conflict_lane.cars[0]
                if conflict_car.lane_group == "T":
                    through_time = conflict_lane.release_time(car) + self.pT
                    if abs(through_time - self.pL) <= .1:
                        conflict_release_time.append(through_time)

            wait_time = max(conflict_release_time)
            if wait_time < self.granted_time:
                used_time += self._release_car(car)
            used_time += wait_time
        return used_time

    def _release_right_group(self, car):
        used_time = 0
        # consider pedestrian
        if self.first_right:
            used_time += self.pedestrian_time
            self.first_right = False

        used_time += self._release_car(car)
        return used_time

    def _release_through_group(self, car):
        return self._release_car(car)