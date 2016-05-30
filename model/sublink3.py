from lane import Lane
from time import Time
from sublink import SubLink


class SubLink3(SubLink):
    def __init__(self, link, lanes):
        self.link = link
        self.lanes = []
        self.capacity = 0
        self.init_lanes(lanes)

        self.timer = 0
        self.pT, self.pL = 1.6, 2.4
        self.headway = [2.98, 2.59, 2.13, 1.91, 1.86, 1.65]
        self.pedestrian_time = 2

    def init_lanes(self, lanes):
        for lane_type, cap in lanes:
            if not cap: continue

            lane = Lane(cap)
            lane.link = self.link
            lane.type = lane_type
            self.lanes.append(lane)

    @property
    def car_num(self):
        return sum([lane.car_num for lane in self.lanes])

    def group_capacity(self, group):
        return sum([lane.empty_space for lane in self.lanes if group in lane.type])

    def find_available_lanes(self, group):
        return [(i, lane) for i, lane in enumerate(self.lanes) if lane.empty_space and group in lane.type]

    def release_cars(self, granted_time):
        for lane in self.lanes:
            lane.release_cars(granted_time)