import random
from sublink import SubLink


class SubLink2(SubLink):
    def __init__(self, link, lane_num):
        SubLink.__init__(self, link, lane_num)
        self.allowed_merge = {"L": lane_num, "R": lane_num, "T": lane_num}
        self.pass_count = 0

    @property
    def next_link(self):
        return self.link.sublink3

    def add_car(self, car, from_lane):
        # if car reaches the zone
        if self.in_zone(car):
            self.lanes[from_lane].append(car)
            car.distance = 0
            self.pass_count += 1
            return True
        return False

    def in_zone(self, car):
        car.distance += self.link.avg_speed * 10.0 / 3600
        return car.distance > self.get_abscissa() or self.link.length >= 200

    def get_abscissa(self):
        return self.link.length - max([len(l) for l in self.lanes]) / self.link.jam_density

    def release_cars(self):
        car_released = True
        while car_released:
            car_released = False
            for lane_number, lane in enumerate(self.lanes):
                if not lane or lane[0].is_blocked:
                    break

                car = lane[0]
                available_lane = self.find_available_lane(car, lane_number)
                if available_lane:
                    available_lane.add(self.__release_car(lane_number))
                    car_released = True
                else:
                    car.set_blocked("No space left on merging zone. %d"
                                    % (self.next_link.group_capacity(car.lane_group)))
        # reset car status for next time stamp
        for lane in self.lanes:
            for car in lane:
                car.unset_blocked()

    def __release_car(self, lane_number):
        car = self.lanes[lane_number].pop(0)
        self.link.notify_observers("Adding car %s to merging group %s"
                                   % (car, car.lane_group))
        return car

    def find_available_lane(car, lane_number):
        available_lanes = self.next_link.find_available_lanes(car.lane_group)
        if not available_lanes:
            return None

        if car.lane_group == "L":
            i, lane = available_lanes.pop()
            if lane.type == "L" and i + 1 < len(self.next_link.lanes()):
                if self.next_link.lanes[i + 1].empty_space:
                    return lane
            else:
                return lane
        elif car.lane_group == "R":
            i, lane = available_lanes.pop()
            if lane.type == "R" and i - 1 >= 0:
                if self.next_link.lanes[i - 1].empty_space:
                    return lane
            else:
                return lane
        else:
            lanes = [lane for (i, lane) in available_lanes if abs(lane_number - i) < 2]
            return random.sample(lanes, 1)[0]